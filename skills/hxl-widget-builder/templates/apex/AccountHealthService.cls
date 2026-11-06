/**
 * Invocable action that returns account health for an HXL widget.
 * Works for both scenarios:
 *  - Agentforce action output  -> Apex-based CLT: @apexClassType/c__AccountHealthService$AccountHealth
 *  - MCP tool output           -> payload CLT property "accountHealth" typed to the same inner class
 * Must be global for hosted MCP server tools.
 */
global with sharing class AccountHealthService {

    global class Request {
        @InvocableVariable(label='Account Name' description='Name (or part of the name) of the account' required=true)
        global String accountName;
    }

    global class Response {
        // The @InvocableVariable NAME ("accountHealth") becomes the MCP payload CLT property name.
        @InvocableVariable(label='Account Health' description='Structured account health')
        global AccountHealth accountHealth;
    }

    // Display-ready values (labels, variants, fallbacks) are computed HERE, not in widget
    // formulas: in the MCP channel the wrapper renderer only remaps plain {!$attrs.x}
    // bindings, so a formula like IF($attrs.isAtRisk, ...) breaks at render time.
    global class AccountHealth {
        @AuraEnabled global String accountName;
        @AuraEnabled global String industry;            // 'Industry not set' when blank
        @AuraEnabled global Decimal annualRevenue;
        @AuraEnabled global String annualRevenueLabel;  // e.g. "USD 25M"
        @AuraEnabled global Integer openCaseCount;
        @AuraEnabled global Boolean isAtRisk;
        @AuraEnabled global String statusLabel;         // 'At risk' | 'Healthy'
        @AuraEnabled global String statusVariant;       // tile/badge variant: 'warning' | 'success'
        @AuraEnabled global String riskReason;
        @AuraEnabled global String recordUrl;
        @AuraEnabled global List<Opp> openOpportunities;
    }

    global class Opp {
        @AuraEnabled global String name;
        @AuraEnabled global String stageName;
        @AuraEnabled global Decimal amount;
        @AuraEnabled global String amountLabel;         // e.g. "120k"
        @AuraEnabled global String closeDate;           // ISO yyyy-MM-dd string
    }

    private static final Integer CASE_RISK_THRESHOLD = 5;

    @InvocableMethod(
        label='Get Account Health'
        description='Returns health for one account: revenue, open cases, risk flag and open opportunities. Use when the user asks how an account is doing.'
    )
    global static List<Response> getAccountHealth(List<Request> requests) {
        List<Response> results = new List<Response>();
        for (Request req : requests) {
            results.add(buildResponse(req.accountName));
        }
        return results;
    }

    private static Response buildResponse(String accountName) {
        Response res = new Response();
        String pattern = '%' + String.escapeSingleQuotes(accountName == null ? '' : accountName.trim()) + '%';

        List<Account> accts = [
            SELECT Id, Name, Industry, AnnualRevenue,
                   (SELECT Name, StageName, Amount, CloseDate
                      FROM Opportunities
                     WHERE IsClosed = false
                     ORDER BY CloseDate ASC
                     LIMIT 5)
              FROM Account
             WHERE Name LIKE :pattern
             ORDER BY LastModifiedDate DESC
             LIMIT 1
        ];
        if (accts.isEmpty()) {
            return res; // accountHealth stays null; agent can say "not found"
        }
        Account a = accts[0];

        Integer openCases = [SELECT COUNT() FROM Case WHERE AccountId = :a.Id AND IsClosed = false];

        AccountHealth h = new AccountHealth();
        h.accountName = a.Name;
        h.industry = String.isBlank(a.Industry) ? 'Industry not set' : a.Industry;
        h.annualRevenue = a.AnnualRevenue;
        h.annualRevenueLabel = UserInfo.getDefaultCurrency() + ' ' + formatMoney(a.AnnualRevenue);
        h.openCaseCount = openCases;
        h.recordUrl = URL.getOrgDomainUrl().toExternalForm() + '/' + a.Id;
        h.openOpportunities = new List<Opp>();

        Boolean overdue = false;
        for (Opportunity o : a.Opportunities) {
            Opp item = new Opp();
            item.name = o.Name;
            item.stageName = o.StageName;
            item.amount = o.Amount;
            item.amountLabel = formatMoney(o.Amount);
            item.closeDate = o.CloseDate == null ? null : String.valueOf(o.CloseDate);
            h.openOpportunities.add(item);
            if (o.CloseDate != null && o.CloseDate < Date.today()) {
                overdue = true;
            }
        }

        List<String> reasons = new List<String>();
        if (openCases > CASE_RISK_THRESHOLD) {
            reasons.add(openCases + ' open cases');
        }
        if (overdue) {
            reasons.add('open opportunities past close date');
        }
        h.isAtRisk = !reasons.isEmpty();
        h.riskReason = h.isAtRisk ? String.join(reasons, '; ') : null;
        h.statusLabel = h.isAtRisk ? 'At risk' : 'Healthy';
        h.statusVariant = h.isAtRisk ? 'warning' : 'success';

        res.accountHealth = h;
        return res;
    }

    private static String formatMoney(Decimal amt) {
        Decimal v = amt == null ? 0 : amt;
        if (v >= 1000000) {
            return (v / 1000000).setScale(1, RoundingMode.HALF_UP).stripTrailingZeros().toPlainString() + 'M';
        }
        return (v / 1000).setScale(0, RoundingMode.HALF_UP).toPlainString() + 'k';
    }
}

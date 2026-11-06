@IsTest
private class AccountHealthServiceTest {

    @TestSetup
    static void setup() {
        Account a = new Account(Name = 'Nordic Test Energy', Industry = 'Energy', AnnualRevenue = 25000000);
        insert a;
        insert new Opportunity(Name = 'Overdue Renewal', AccountId = a.Id, StageName = 'Prospecting',
                               Amount = 120000, CloseDate = Date.today().addDays(-3));
        List<Case> cases = new List<Case>();
        for (Integer i = 0; i < 6; i++) {
            cases.add(new Case(AccountId = a.Id, Subject = 'Issue ' + i, Status = 'New'));
        }
        insert cases;
    }

    @IsTest
    static void returnsHealthAndFlagsRisk() {
        AccountHealthService.Request req = new AccountHealthService.Request();
        req.accountName = 'Nordic Test';

        Test.startTest();
        List<AccountHealthService.Response> res =
            AccountHealthService.getAccountHealth(new List<AccountHealthService.Request>{ req });
        Test.stopTest();

        AccountHealthService.AccountHealth h = res[0].accountHealth;
        System.assertNotEquals(null, h, 'Account should be found');
        System.assertEquals(6, h.openCaseCount);
        System.assertEquals(1, h.openOpportunities.size());
        System.assert(h.isAtRisk, 'Should be at risk');
        System.assertEquals('At risk', h.statusLabel);
        System.assertEquals('warning', h.statusVariant);
        System.assert(h.annualRevenueLabel.endsWith('25M'), 'Revenue label formatted: ' + h.annualRevenueLabel);
        System.assertEquals('120k', h.openOpportunities[0].amountLabel);
        System.assert(h.recordUrl.contains('/'), 'Record URL populated');
    }

    @IsTest
    static void handlesUnknownAccount() {
        AccountHealthService.Request req = new AccountHealthService.Request();
        req.accountName = 'Does Not Exist 123';
        List<AccountHealthService.Response> res =
            AccountHealthService.getAccountHealth(new List<AccountHealthService.Request>{ req });
        System.assertEquals(null, res[0].accountHealth);
    }
}

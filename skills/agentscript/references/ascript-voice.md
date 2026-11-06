# Configure Voice Models in Agent Script

Agentforce voice-enabled agents use two speech models: a speech-to-text (STT) model that listens to the customer, and a text-to-speech (TTS) model that speaks the agent's responses. You choose them independently in the `modality voice` block of Agent Script. The Canvas view of Agentforce Builder refers to these as the *listening* model and the *speaking* model. In Agent Script, you configure them in the `inbound` and `outbound` sections.

The default models depend on the configured locale and the capabilities enabled for your org. Check the available models and compatible persona for your target locale before adding an override.

## How Voice Selection Works

An Agentforce Voice agent makes two independent model choices:

- **Listening model (`inbound`)**: the speech-to-text engine that turns the customer's speech into text, such as Deepgram Nova-3 or Kotoba STT.
- **Speaking model (`outbound`)**: the text-to-speech engine that generates the agent's speech, such as ElevenLabs v3 Conversational or Kotoba TTS.

`inbound` and `outbound` describe the direction of the audio, not whether the call is incoming or outgoing. Inbound is what the agent hears from the customer. Outbound is what the agent says.

Changing one model doesn't change the other. For example, you can keep the default listening model and switch the speaking model for one language.

A **voice persona** is the specific voice (the tone, accent, and character) that a speaking model uses. Personas belong to speaking models. Listening models don't have personas.

## Models for Listening (Inbound, Speech-to-Text)

Specify a listening model by its model ID in the `inbound.model.id` property.

| Listening Model | Model ID            | Choose it for                                                   |
| :-------------- | :------------------ | :-------------------------------------------------------------- |
| Deepgram Nova-3 | `nova-3`            | General speech recognition. Works with the `keywords` property. |
| Kotoba STT      | `EinsteinKotobaSTT` | Japanese speech recognition (Japanese).                         |

If you don't select a listening model, the agent uses the default for your configured locale. To set a listening model, see [Configure Listening](#configure-listening-inbound).

### Capture IDs and Codes Spoken Letter by Letter

When a caller spells out an ID, code, or reservation number, some listening models write the letter O as the digit 0. If your agent collects IDs, codes, or reservation numbers in languages other than English, add instructions to the agent that explain the format of the ID and how to handle a 0 where a letter is expected. Real zeros are valid in IDs, so don't tell the agent to replace every 0. Instead, have the agent read the ID back and confirm any character that could be an O or a 0.

## Models for Speaking (Outbound, Text-to-Speech)

Agentforce Voice supports these speaking models. Choose the one that fits your agent:

| Speaking Model               | Model ID                   | Choose it for                                                                                                                                                                                                                                                                                                       |
| :--------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ElevenLabs v3 Conversational | `eleven_v3_conversational` | The most natural, expressive speech, and reliable pronunciation of entities like numbers, email addresses, and IDs. These voices are better than v2.5 for most languages. The default for most languages.                                                                                                           |
| ElevenLabs Flash v2          | `eleven_flash_v2`          | Better quality English than Flash v2.5, with steadier non-US English accents than v3 Conversational. Supports IPA phoneme pronunciation rules; CMU support isn't confirmed. Honors the `speed`, `stability`, and `similarity` parameters. English locales only.                                                     |
| ElevenLabs Flash v2.5        | `eleven_flash_v2_5`        | The counterpart to Flash v2 for languages other than English: the best adherence for secondary accents, such as Argentinian Spanish, French Canadian, and European Portuguese. Lower latency; honors the `speed`, `stability`, and `similarity` parameters. Doesn't support IPA or CMU phoneme pronunciation rules. |
| Kotoba TTS                   | `kotoba`                   | Japanese speech.                                                                                                                                                                                                                                                                                                    |

Use an explicit supported model when you need its particular capabilities, such as latency, language, accent behavior, or custom pronunciation, and verify the resulting voice through the intended channel.

You can select a non-default model only in Agent Script. Agentforce Builder (Canvas) doesn't yet expose a voice-model selector, so v3 Conversational (the default) is the only model available there. To use Flash v2, Flash v2.5, or Kotoba on a non-default language, override the model in the `modality voice` block.

### Which Model Should I Use?

Change the voice model only when the locale's default model doesn't meet your needs.

Consider these tradeoffs when you choose between ElevenLabs v3 Conversational and the Flash models:

- **ElevenLabs v3 Conversational** is the strongest all-around model and the default for most languages. It's the most expressive, and it pronounces entities like numbers, email addresses, and IDs correctly out of the box. However, it's less reliable with some non-US English accents, such as UK and Australian English. It doesn't use the `speed` or `similarity` parameters. `stability` defaults to 0.5.
- **ElevenLabs Flash v2** is English-only and the best choice for English. It supports IPA and CMU phoneme pronunciation rules, produces higher-quality English than Flash v2.5, and handles non-US English accents, such as UK and Australian English, more stably than v3 Conversational. It has lower latency and honors the `speed`, `stability`, and `similarity` parameters. Choose it when you want faster responses, fine-grained control over how a voice sounds, or IPA and CMU pronunciation rules for an English agent.
- **ElevenLabs Flash v2.5** is the counterpart to Flash v2, for languages other than English. It gives the best adherence for secondary accents, such as Argentinian Spanish, French Canadian, and European Portuguese. It has lower latency and honors the `speed`, `stability`, and `similarity` parameters. It doesn't support IPA or CMU phoneme pronunciation rules. If you need phoneme pronunciation rules and your agent is in English, use Flash v2.

### Choosing a Voice

You choose a voice in two steps, because each voice persona is listed under the models it supports:

1. **Choose a speaking model.** To use a model other than the language default, set it in the `outbound.model` section of the `modality voice` block.
2. **Choose a voice persona from that model's voice list.** Each model publishes its own set of voices and the languages each voice supports. Find the voice you want in that model's list, and then set its **hash ID** as the `persona_id`. Use the hash ID as the identifier. The same voice used with a different model counts as a distinct voice, so match the hash ID to your selected model.

See [Supported Voice Models](#supported-voice-models) for the voice list and supported languages for each model.

You can keep using the locale's default model without any changes. To use a different supported model, override it in the `modality voice` block of your Agent Script.

:::note
**Test a voice before you commit to it.** The CLI preview is text only. It checks that your agent runs, but not how the voice sounds. To hear a voice, use Voice Preview in the browser. A voice sounds different in a live conversation than in a static sample, so evaluate the voice through the channel your customers use.

When you set a voice model in Agent Script, don't switch back to Agentforce Builder (Canvas) to change the voice and then return to the script. Canvas and Agent Script use different underlying formats, and moving between them can leave your voice configuration in an inconsistent state.
:::

## Modality Voice Block

The `modality voice` block defines how your agent listens and speaks. It has two directions, both optional. Configure only the ones you need:

- `inbound` (listening): how the agent listens, including the speech-to-text (STT) model and keyword and filler-word detection.
- `outbound` (speaking): how the agent speaks, including the voice persona, the text-to-speech (TTS) model, and model parameters such as speed and stability.

This example configures both directions:

```sfdocs-code {"lang":"agentscript", "title": "Modality Voice Block"}
modality voice:
    inbound: # listening
        keywords:
            - "urgent"
            - "emergency"
    outbound: # speaking
        persona_id: "8438b254ab85" # Lucie (fr), a Flash v2.5 voice
        model:
            id: "eleven_flash_v2_5"
            parameters:
                speed: 1.0
                stability: 0.8
```

## Configure Listening (Inbound)

The `inbound` section configures how the agent listens to the customer, including the speech-to-text (STT) model. See [Models for Listening](#models-for-listening-inbound-speech-to-text) for the available models.

```sfdocs-code {"lang":"agentscript", "title": "Inbound Voice"}
modality voice:
    inbound:
        keywords:
            - "urgent"
            - "emergency"
        model:
            id: "nova-3"
```

These properties make up the `inbound` section:

| Property                 | Description                                                                                                                               | Default |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `filler_words_detection` | Optional. When `True`, filler words such as "um" and "uh" are included in the transcript. When `False`, common filler words are left out. | `False` |
| `keywords`               | Optional. A list of keywords to boost during recognition, which improves accuracy for domain-specific terms.                              | —       |
| `model`                  | Optional. Selects and configures the speech-to-text model. Omit to use the default.                                                       | Default |
| `model.id`               | Optional. The model ID of the speech-to-text model, such as `nova-3`.                                                                     | Default |
| `model.parameters`       | Optional. Model-specific settings passed through to the speech-to-text model.                                                             | —       |

### Select the Kotoba STT Model for Japanese

```sfdocs-code {"lang":"agentscript", "title": "Select the Kotoba STT Model"}
modality voice:
    inbound:
        model:
            id: "EinsteinKotobaSTT"
```

In testing, `kana` set to `false` returned kanji, and `kana` set to `true` returned katakana. When both a language-specific setting and a common setting are present, the language-specific setting takes priority.

### Use a Different Listening Model for One Language

To use a different listening model for one language, put the `inbound` override in that language's `language_settings` entry. Other declared languages keep the agent-level listening settings. See [Per-Language Voice Settings](#per-language-voice-settings).

```sfdocs-code {"lang":"agentscript", "title": "Per-Language Listening Override"}
language:
    default_locale: "en_US"
    additional_locales: "ja"
modality voice:
    language:
        default_locale: "en_US"
        additional_locales: "ja"
    language_settings:
        ja: # Japanese only
            inbound:
                model:
                    id: "EinsteinKotobaSTT"
```

This sets the model for that language. It doesn't by itself decide which language a caller hears.

## Configure Speaking (Outbound)

The `outbound` section sets the voice persona, the speaking (TTS) model, and any model parameters. See [Models for Speaking](#models-for-speaking-outbound-text-to-speech) for the available models.

```sfdocs-code {"lang":"agentscript", "title": "Outbound Voice"}
modality voice:
    outbound:
        persona_id: "dd0c9186f164" # Olivia (en_US), a v3 Conversational voice
```

These properties make up the `outbound` section:

| Property           | Description                                                                                                                                                                                                                            | Default              |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------- |
| `persona_id`       | Optional. The identifier of the voice persona the agent speaks with. Use the **hash ID** from the [Voice Catalog](ascript-voice-catalog.md) for your selected model. Omit to use the locale's default voice. | Locale default voice |
| `model`            | Optional. Selects and configures the voice model. Omit to use the language's default model.                                                                                                                                            | Language default     |
| `model.id`         | Optional. The model ID of the voice model to use, such as `eleven_flash_v2_5`. Omit to use the language's default model. See [Supported Voice Models](#supported-voice-models) for the available model IDs.                            | Language default     |
| `model.parameters` | Optional. Model-specific settings passed through to the voice model. See [Model Parameters](#model-parameters).                                                                                                                        | —                    |
| `pronunciations`   | Optional. The pronunciation dictionary for the agent. See [Pronunciation Dictionary](#pronunciation-dictionary).                                                                                                                       | —                    |

### Model Parameters

`model.parameters` accepts scalar values, such as strings, booleans, or numbers. Agent Script accepts them without checking every model-specific name or range, so a successful compile doesn't mean a parameter took effect. Which parameters a model honors, and their valid ranges, are defined by the model itself, and the runtime can filter or ignore a parameter the model doesn't recognize.

These parameters are commonly used with the ElevenLabs voice models. Treat this as a starting point, not a complete or enforced list.

Each voice persona ships with its own tuned defaults for these parameters, so a value that sounds right for one persona isn't the default for another. Omit a parameter to use the persona's default, and set one only when you want to override it.

The ranges below apply to the ElevenLabs Flash v2.5 and Flash v2 models, which honor these parameters. ElevenLabs v3 Conversational doesn't use `speed` or `similarity`, so their ranges don't apply to it.

| Parameter    | Description                                                                                                                    | Range   |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------- | :------ |
| `speed`      | How fast the voice speaks. Lower values slow the speech down; higher values speed it up.                                       | 0.7–1.2 |
| `stability`  | How consistent the delivery is. Lower values give a more expressive, variable performance; higher values give steadier speech. | 0–1     |
| `similarity` | How closely the output matches the original voice's character. Higher values stay closer to the source voice.                  | 0–1     |

How a model applies these parameters varies:

- **ElevenLabs Flash v2.5 and Flash v2** honor `speed`, `stability`, and `similarity`. Use a Flash model when you need precise control over how a voice sounds.
- **ElevenLabs v3 Conversational** doesn't use `speed` or `similarity`. `stability` defaults to 0.5.
- **Kotoba** doesn't take these parameters. Select the model and a persona without a `parameters` block.

### Pronunciation Dictionary

A pronunciation dictionary tells the voice model how to say specific words. Set it once in `pronunciations` inside the `outbound` section, and it applies to the agent:

```sfdocs-code {"lang":"agentscript", "title": "Pronunciation Dictionary"}
modality voice:
    outbound:
        pronunciations:
            - grapheme: "API"
              phoneme: "bəˈnænə"
              type: "IPA"
```

| Property   | Description                                |
| :--------- | :----------------------------------------- |
| `grapheme` | The written word.                          |
| `phoneme`  | How to say the word, in IPA or CMU.        |
| `type`     | The phonetic alphabet: `"IPA"` or `"CMU"`. |

Include all three properties in every entry, and use uppercase `IPA` or `CMU`. A missing `grapheme` or `phoneme` causes an error. A missing `type` silently drops the entry, so a successful compile doesn't prove the pronunciation was kept.

Custom pronunciation is a capability of the voice model, so support depends on the model you select:

| Voice Model                  | IPA and CMU phoneme rules        |
| :--------------------------- | :------------------------------- |
| ElevenLabs v3 Conversational | IPA supported; CMU not confirmed |
| ElevenLabs Flash v2          | IPA supported; CMU not confirmed |
| ElevenLabs Flash v2.5        | Not supported                    |
| Kotoba TTS                   | Not documented                   |

Use straight double quotes around the phoneme value, and uppercase `"IPA"` for the type. Results vary by voice, language, and context, so test important terms on the phone channel.

Even when a model supports phoneme rules, pronunciation quality can vary by language, and an override doesn't guarantee the result you want in every language. A pronunciation block that compiles doesn't establish that the selected model applies it to speech. Test your terms with your chosen model, voice, and language through your intended channel.

Use the agent-level dictionary by default. Add `pronunciations` to a `language_settings` entry only when a word needs to be said differently in one language. See [Per-Language Voice Settings](#per-language-voice-settings).

### Select the Flash v2 Voice Model

Flash v2 is the English-only, lower-latency model, and it's the best choice for English agents. It supports IPA phoneme pronunciation rules (CMU support isn't confirmed) and handles non-US English accents, such as UK and Australian English, more stably than v3 Conversational. Like Flash v2.5, it honors the `speed`, `stability`, and `similarity` parameters. To use it, specify the Flash v2 model and a compatible English voice persona in the `modality voice` block. No other Agent Script blocks need to change.

Use Flash v2 for English. For other languages, use Flash v2.5 instead.

```sfdocs-code {"lang":"agentscript", "title": "Select the Flash v2 Voice Model"}
modality voice:
    outbound:
        persona_id: "a029af9d692c" # April (en_US), a Flash v2 voice
        model:
            id: "eleven_flash_v2"
            parameters:
                speed: 1.0
                stability: 0.8
                similarity: 0.75
```

### Select a Flash v2.5 Voice Model

Flash v2.5 is the lower-latency model for languages other than English, so it's a good fit when you want faster spoken responses. It gives the best adherence for secondary accents, such as Argentinian Spanish, French Canadian, and European Portuguese. Unlike v3 Conversational, it honors the `speed`, `stability`, and `similarity` parameters, so choose it when you also want fine-grained control over how a voice sounds. Flash v2.5 doesn't support IPA or CMU phoneme pronunciation rules. To use it, specify the Flash v2.5 model and a compatible Flash v2.5 voice persona in the `modality voice` block. No other Agent Script blocks need to change.

Use Flash v2.5 for non-English languages. For English, use Flash v2 instead.

```sfdocs-code {"lang":"agentscript", "title": "Select the Flash v2.5 Voice Model"}
modality voice:
    outbound:
        persona_id: "4f708167ff27" # Louis (fr), a Flash v2.5 voice
        model:
            id: "eleven_flash_v2_5"
            parameters:
                speed: 1.0
                stability: 0.8
                similarity: 0.75
```

### Select the Kotoba TTS Model for Japanese

To use Kotoba TTS, specify the model and a compatible Japanese voice persona. Kotoba doesn't take voice parameters, so omit the `parameters` block.

```sfdocs-code {"lang":"agentscript", "title": "Select the Kotoba TTS Model"}
modality voice:
    language:
        default_locale: "ja"
    language_settings:
        ja:
            outbound:
                persona_id: "e5d63b40f254" # Azawa (ja), a Kotoba voice
                model:
                    id: "kotoba"
```

Test this setup on the phone channel. In phone conversations, with English as the text default and Japanese as the voice default, Japanese replies can be cut off.

## Per-Language Voice Settings

Declare your languages once in the `language` block, and then override voice settings for any one of them in `language_settings`. The `inbound` (listening) and `outbound` (speaking) settings in `modality voice` apply to every language. Each `language_settings` entry overrides them for one declared language, in either direction.

Declare each language that has an override in a `language` block inside `modality voice`, too. This voice-specific block can use only languages from the top-level `language` block.

```sfdocs-code {"lang":"agentscript", "title": "Per-Language Voice Override"}
language:
    default_locale: "en_US"
    additional_locales: "fr"
modality voice:
    language: # voice languages
        default_locale: "en_US"
        additional_locales: "fr"
    outbound: # every language
        model:
            id: "eleven_flash_v2"
    language_settings:
        fr: # French only
            outbound:
                persona_id: "<French voice ID>"
                model:
                    id: "eleven_flash_v2_5"
```

In this example, French overrides the voice and model, and inherits the rest.

## Change an Existing Agent

To change the listening or speaking model of an existing agent:

1. Open the agent's Agent Script.
2. In the `modality voice` block, set `inbound.model.id` to change the listening model, or `outbound.model.id` to change the speaking model. If you change the speaking model, also check that your `persona_id` is supported by that model. Use the [voice list](#voice-lists) for that model to confirm.
3. Use the nested format described in this topic. If the block still has legacy keys, convert them first. See [Legacy-to-Nested Key Map](#legacy-to-nested-key-map).
4. Validate the script, save it, and publish the agent.

## Verify the Change

A script that compiles doesn't prove the agent uses the models you selected. The CLI preview is text only, so it can't confirm audio behavior. Use Voice Preview in the browser or a live call to check how the voice sounds.

1. Validate the script and fix any errors.
2. Call the agent through the voice channel your customers use.
3. Listen for the voice you chose, and check that the agent understands the terms you expect, such as product names and keywords.

## Legacy Voice Format

Some existing scripts use an older, flat format that sets a voice and speed directly, without the `outbound` and `model` nesting:

```sfdocs-code {"lang":"agentscript", "title": "Legacy Voice Format"}
modality voice:
    voice_id: "<voice identifier>"
    outbound_speed: 0.9
```

This format still works, so scripts that use it keep running without changes. But it can't select a voice model such as Flash v2.5. Model selection exists only in the nested format. For any new voice configuration, use the nested format shown earlier.

:::important
Use one voice format within a `modality voice` block. If you migrate to the nested format, remove all legacy voice properties from that block. There's no automatic conversion.
:::

### Legacy-to-Nested Key Map

| Legacy key                       | Nested path                                                                                                                                                                                                         |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `voice_id`                       | `outbound.persona_id`. A legacy `voice_id` is often a 20-character ElevenLabs voice ID, which isn't a `persona_id`. Use an identifier from the [Voice Catalog](ascript-voice-catalog.md). |
| `outbound_speed`                 | `outbound.model.parameters.speed`                                                                                                                                                                                   |
| `outbound_stability`             | `outbound.model.parameters.stability`                                                                                                                                                                               |
| `outbound_similarity`            | `outbound.model.parameters.similarity`                                                                                                                                                                              |
| `outbound_style_exaggeration`    | No nested replacement. Remove it. A `style` value in `outbound.model.parameters` compiles, but whether it has any effect depends on the voice model.                                                                |
| `inbound_filler_words_detection` | `inbound.filler_words_detection`                                                                                                                                                                                    |
| `inbound_keywords`               | `inbound.keywords`. Drop the extra `keywords` wrapper so the value is a list of strings.                                                                                                                            |
| `outbound_filler_sentences`      | `outbound.filler_sentences`                                                                                                                                                                                         |
| `pronunciation_dict`             | `outbound.pronunciations`. Each entry needs `grapheme`, `phoneme`, and `type`.                                                                                                                                      |

`additional_configs` isn't in the table because both formats share it. Keep it directly under `modality voice`.

### Troubleshoot the Mixed-Format Error

The nested properties are `inbound`, `outbound`, `language`, and `language_settings`. If a `modality voice` block contains any of them alongside any legacy key, the compiler rejects the block. A separate top-level `language` block doesn't trigger the error, and `additional_configs` isn't a legacy-only marker.

The compiler can report:

```
Invalid modality voice configuration. Both Voice schema versions were detected, use only one at a time.
```

It can also identify a specific legacy property. For example:

```
Cannot mix V1 and V2 voice properties. 'outbound_speed' is a V1 property but V2 properties are also present: inbound, outbound, language. Use exclusively V1 or V2 properties.
```

The property name and the list of nested properties vary with the script. To fix the error, convert every legacy key in the block using the table above, and delete the legacy keys.

## Supported Voice Models

These are the speaking (TTS) models. Specify a model by its model ID in `outbound.model.id`. For listening (STT) models, see [Models for Listening](#models-for-listening-inbound-speech-to-text).

| Speaking Model               | Model ID                   | Availability                                                       | Voice List                                                                                                  |
| :--------------------------- | :------------------------- | :----------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| ElevenLabs v3 Conversational | `eleven_v3_conversational` | Default for most languages. Available in Canvas and Agent Script.  | [ElevenLabs v3 Conversational Voices](ascript-voice-catalog-v3-conversational.md) |
| ElevenLabs Flash v2.5        | `eleven_flash_v2_5`        | For languages other than English. Selectable in Agent Script only. | [ElevenLabs Flash v2.5 Voices](ascript-voice-catalog-flash-2-5.md)                |
| ElevenLabs Flash v2          | `eleven_flash_v2`          | English only. Selectable in Agent Script only.                     | [ElevenLabs Flash v2 Voices](ascript-voice-catalog-flash-2.md)                    |
| Kotoba TTS                   | `kotoba`                   | Japanese (`ja`) only.                                              | [Kotoba Voices](ascript-voice-catalog-kotoba.md)                                  |

When you don't select a model, the agent uses the default for the configured locale. To use a non-default model, select it in the `modality voice` block. Canvas doesn't yet expose a voice-model selector. For how each model handles voice parameters, see [Model Parameters](#model-parameters).

## Voice Lists

Each model has its own catalog of voice personas, and each voice supports specific locales:

- [ElevenLabs v3 Conversational Voices](ascript-voice-catalog-v3-conversational.md)
- [ElevenLabs Flash v2 Voices](ascript-voice-catalog-flash-2.md)
- [ElevenLabs Flash v2.5 Voices](ascript-voice-catalog-flash-2-5.md)
- [Kotoba Voices](ascript-voice-catalog-kotoba.md)

For all lists on one page, see the full [Voice Catalog for Agentforce Voice](ascript-voice-catalog.md).

To set a voice, find it in the list for your selected model and use its hash ID as the `persona_id`. If you don't set a `persona_id`, the agent uses the locale's default voice, marked **(default)** in the voice list.

## Respond When a Caller Interrupts

When a caller cuts off the agent mid-reply (barges in), the agent can re-ask for details the caller already confirmed, or go off script. To prevent this, check the `@system_variables.last_reply` system variable in your reasoning instructions. It tells the agent whether the caller interrupted its last reply, and what part of that reply the caller heard. See [System Variables: last_reply](reference/ascript-ref-variables-system.md#last_reply).

## Sample Voice Configuration

This example combines the four parts of a voice configuration:

1. `language`: which languages the agent speaks.
2. `modality voice`: how the agent speaks and listens, for every language, plus the voice languages that have overrides.
3. `language_settings`: overrides for one declared language.
4. `pronunciations`: the pronunciation dictionary, inside the agent-level `outbound` settings.

```sfdocs-code {"lang":"agentscript", "title": "Combined Voice Configuration"}
language: # 1
    default_locale: "en_US"
    additional_locales: "fr"
modality voice: # 2
    language: # voice languages
        default_locale: "en_US"
        additional_locales: "fr"
    outbound: # speaking, all languages
        persona_id: "<English voice ID>"
        model:
            id: "eleven_flash_v2"
        pronunciations: # 4
            - grapheme: "Eliquis"
              phoneme: "ɛlɪkwɪs"
              type: "IPA"
    language_settings: # 3
        fr:
            outbound:
                persona_id: "<French voice ID>"
                model:
                    id: "eleven_flash_v2_5"
```

On a call:

- **English:** Flash v2, the English voice, and "Eliquis" said the dictionary's way.
- **French:** The French voice on Flash v2.5, with the rest inherited.

## Considerations

- Existing agents and existing Agent Script continue to work without changes. To use the new voice capabilities, rewrite the `modality voice` block.
- You can't mix the legacy and nested voice formats in the same `modality voice` block. See [Troubleshoot the Mixed-Format Error](#troubleshoot-the-mixed-format-error).
- Agentforce Builder (Canvas) doesn't expose a voice-model selector, doesn't show the voice catalog for non-default models, and doesn't filter its voice picker based on an Agent Script override.

## Related Topics

- [Agent Script Blocks](ascript-blocks.md)
- [Agent Script Reference](reference/ascript-reference.md)
- [Agent Script Reference: System Variables](reference/ascript-ref-variables-system.md)
- [ElevenLabs](https://elevenlabs.io/)

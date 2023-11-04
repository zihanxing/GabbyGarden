'<speak>'

\- Usage: The root element of the SSML response. The content within the token will be spoken

\- example:  

<speak>my SSML content </speak>

## -------------------------------

'<break>'

-Usage: An empty element that controls pausing or other prosodic boundaries between words. Using `<break>` between any pair of tokens is optional. If this element is not present between words, the break is automatically determined based on the linguistic context.

-example: 

```
<speak>
  Step 1, take a deep breath. <break time="200ms"/>
  Step 2, exhale.
  Step 3, take a deep breath again. <break strength="weak"/>
  Step 4, exhale.
</speak>
```



## ` `<say‑as> 

-Usage: This element lets you indicate information about the type of text construct that is contained within the element. It also helps specify the level of detail for rendering the contained text. The `<say‑as>` element has the required attribute, `interpret-as`, which determines how the value is spoken. Optional attributes `format` and `detail` may be used depending on the particular `interpret-as` value.

-example: 

The `interpret-as` attribute supports the following values:

- currency

 

 

 
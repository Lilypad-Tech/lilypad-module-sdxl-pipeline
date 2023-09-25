# Example Lilypad Module

Author your own Lilypad module:

Create a file called `lilypad_module.json.tmpl`

This is a json template with Go text/template style `{{.Message}}` sections which will be replaced by Lilypad with valid JSON strings which are passed as input to modules.

Pass inputs as:

```
lilypad run github.com/username/repo:tag -i Message=moo
```

Inputs are a map of strings to strings.

**YOU MUST MAKE YOUR MODULE DETERMINISTIC**

Tips:
* Make the output reproducible, for example for the diffusers library, see [here](https://huggingface.co/docs/diffusers/using-diffusers/reproducibility)
* Strip timestamps and time measurements out of the output, including to stdout/stderr
* Don't read any sources of entropy (e.g. /dev/random)
* When referencing docker images, you MUST specify their sha256 hashes, as shown in this example

If your module is not deterministic, compute providers will not adopt it and add it to their allowlists.

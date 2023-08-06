
# md_inputs

`md_inputs` is a python-mardown extension for inputs(text, select, checkbox...) in markdown document

# Usage

Use [[ text ]] to make a inline input element.

Text must contion attribute: `type` at least, like a html tag, your can add any attribute into the input element.

The `value` attribute is used to set the `checkbox` `radio` `select` input type value(`selected` or `checked` in given index(start from 0 for `selected`), "1" means `checked`)

If the `type` is `select`, the `opt` and `opt_value` attribute is used to set select options. `opt` means the display text of selections, each item use `:` to seperate. `opt_value` is the value of options, the separated item count of the `opt_value` must be the same of the `opt`. if the `opt_value` has not given, md_inputs will use the `opt` instead the `opt_value`.

# Example

## select

### markdown:

````
[[type='select' opt='eopt1:eopt2' class='dfaj' id='eid1']]
````

### html:

```` html
<p><span><select class='dfaj' id='eid1' ><option value='eopt1'>eopt1</option><option value='eopt1'>eopt2</option></select></span></p>
````

### markdown:

````
[[type='select' opt='eopt1:eopt2' opt_value="1:2" class='dfaj' id='eid1' value="1"]]
````

### html:

```` html
<p><span><select class='dfaj' id='eid1' value='1' ><option value='1' >eopt1</option><option value='2' selected>eopt2</option></select></span></p>
````

## input

markdown:

````
[[type='input' value="hello" id='edit1']]
````

html:

```` html
<p><span><input type='input' value='hello' id='edit1' /></span></p>
````

## checkbox

markdown:

````
[[type='checkbox' value="1"]]
````

html:

```` html
<p><span><input type='checkbox' value='1' checked /></span></p>
````

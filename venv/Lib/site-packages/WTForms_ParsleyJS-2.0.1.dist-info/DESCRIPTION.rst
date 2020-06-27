
This is a small library which you can hook into your WTForms form classes in order to
enable client side validation.

WTForms allows you to validate your forms on the server side. Ideally, we could reuse
these validators on the client side with JavaScript without writing any extra code. This
will allow for more direct user feedback in our forms.

This library uses ParsleyJS for this task. ParsleyJS is a popular client side
JavaScript validation library. It is configured using specific HTML markup in the forms.

This library will generate these attributes from your WTForms validators.

For more information consult the README.md in the Github repository at
https://github.com/fuhrysteve/wtforms-parsleyjs




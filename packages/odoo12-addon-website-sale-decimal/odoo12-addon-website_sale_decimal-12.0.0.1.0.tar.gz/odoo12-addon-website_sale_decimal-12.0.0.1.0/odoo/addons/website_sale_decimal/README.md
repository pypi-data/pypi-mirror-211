# Website Sale Decimal

This Odoo module modifies the `website_sale` module to allow decimal quantities in the shopping cart. This is useful for stores that sell items by weight or volume.

It changes the `parseInt` function to `parseFloat` in the `_changeCartQuantity` and `_onChangeCartQuantity` functions, allowing users to specify quantities with decimals.

## Usage

Once installed, this module will automatically change the behavior of the shopping cart in your Odoo website. Users will be able to specify quantities with decimals in their shopping cart.

## Dependencies

This module depends on the `website_sale` module.

## Disclaimer

This module changes the behavior of the shopping cart to handle decimal quantities. Depending on how your Odoo instance and any other modules you have installed handle decimal quantities, this could cause errors or unexpected behavior. Please test this module thoroughly in a non-production environment before installing it in a production environment.

## License

This module is licensed under the AGPL-3.0 License.

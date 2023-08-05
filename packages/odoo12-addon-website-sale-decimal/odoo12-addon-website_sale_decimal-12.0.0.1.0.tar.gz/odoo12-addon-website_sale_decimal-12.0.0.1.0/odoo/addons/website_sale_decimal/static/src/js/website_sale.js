odoo.define('website_sale_decimal.website_sale', function (require) {
    'use strict';

    var sAnimations = require('website.content.snippets.animation');
    var core = require('web.core');
    var _t = core._t;

    sAnimations.registry.WebsiteSale.include({
        _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
            _.each($dom_optional, function (elem) {
                $(elem).find('.js_quantity').text(value);
                productIDs.push($(elem).find('span[data-product-id]').data('product-id'));
            });
            $input.data('update_change', true);

            this._rpc({
                route: "/shop/cart/update_json",
                params: {
                    line_id: line_id,
                    product_id: parseFloat($input.data('product-id'), 10),
                    set_qty: value
                },
            }).then(function (data) {
                $input.data('update_change', false);
                // Updated to use parseFloat instead of parseInt
                var check_value = parseFloat($input.val() || 0);
                if (isNaN(check_value)) {
                    check_value = 1;
                }
                if (value !== check_value) {
                    $input.trigger('change');
                    return;
                }
                var $q = $(".my_cart_quantity");
                if (data.cart_quantity) {
                    $q.parents('li:first').removeClass('d-none');
                }
                else {
                    window.location = '/shop/cart';
                }
    
                $q.html(data.cart_quantity).hide().fadeIn(600);
                $input.val(data.quantity);
                $('.js_quantity[data-line-id='+line_id+']').val(data.quantity).html(data.quantity);
    
                $(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();
                $(".js_cart_summary").first().before(data['website_sale.short_cart_summary']).end().remove();
    
                if (data.warning) {
                    var cart_alert = $('.oe_cart').parent().find('#data_warning');
                    if (cart_alert.length === 0) {
                        $('.oe_cart').prepend('<div class="alert alert-danger alert-dismissable" role="alert" id="data_warning">'+
                                '<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning + '</div>');
                    }
                    else {
                        cart_alert.html('<button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> ' + data.warning);
                    }
                    $input.val(data.quantity);
                }
            });
        },
        _onChangeCartQuantity: function (ev) {
            var $input = $(ev.currentTarget);
            if ($input.data('update_change')) {
                return;
            }
            // Updated to use parseFloat instead of parseInt
            var value = parseFloat($input.val() || 0);
            if (isNaN(value)) {
                value = 1;
            }
            var $dom = $input.closest('tr');
            // var default_price = parseFloat($dom.find('.text-danger > span.oe_currency_value').text());
            var $dom_optional = $dom.nextUntil(':not(.optional_product.info)');
            var line_id = parseInt($input.data('line-id'), 10);
            var productIDs = [parseInt($input.data('product-id'), 10)];
            this._changeCartQuantity($input, value, $dom_optional, line_id, productIDs);
        },
    });
});

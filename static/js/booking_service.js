odoo.define('dym_customer_booking.booking',function (require){
    "use strict";
    var ajax = require('web.ajax');

    $('#city_id').change(function() {
        var city = $(city_id).val();
        
        console.log(city);
        console.log(ajax);
        ajax.jsonRpc('/cek/city', 'call',  {
        'city' : city,
        }).then(function (json_data){
            var branch_rec = json_data['branch_rec'];

            $('#branch_id').empty().append('<option selected="selected" value="False"></option>');
            
            $.each(branch_rec, function (i, item) {
                console.log("hey");
                $('#branch_id').append($('<option>', { 
                    value: item['id'],
                    text : item['display_name'] 
                },'</option>'));
            });

        });    
    });

    $("#tgl_servis").datepicker({
        onSelect: function(dateText) {
            console.log("Selected date: " + dateText + "; input's current value: " + this.value);
        },
        beforeShowDay: function(date) {
            var day = date.getDay();
            return [(day != 0 && day != 6)];
        }
    });
    // $( function() {
    //     $( "#tgl_servis" ).datepicker();
    //     var tgl =  $(tgl_servis).val();
    //     console.log(tgl);
    //   } );
});

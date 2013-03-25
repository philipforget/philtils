/*global window*/
(function () {
    "use strict";
    var github_dif_re = /^https?:\/\/github.com\/.*\/files\/?/;
    console.log('fuck');
    console.log(github_dif_re);

    function initialize_diff_view() {
        function toggle_div($min_button){
            var minimized = $min_button.text() == "+",
                $file = $min_button.parents('.file'),
                $data = $file.find('.data');

            if(minimized){
                $data.show();
                $min_button.html('-');
            }
            else {
                $data.hide();
                $min_button.html('+');
            }
        }

        _.each($('.file'), function(file){
            var diff_div = $(file),
                button_group = $(diff_div.find('.button-group')[0]),
                min_button = $("<a class='minibutton minimize'>-</a>");

            button_group.append(min_button);

            diff_div.on('click', function(e){
                if ($(e.target).is('.minimize')){
                    toggle_div($(e.target));
                }
            });
        });

    }

    // Add some minimize buttons to github diff view
    if (github_dif_re.test(window.location.href)) {
        initialize_diff_view();
    }

}());

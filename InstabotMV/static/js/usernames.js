(function($){
  $(function(){

    $('#insta_us_name').tokenfield({
            autocomplete: {
                source: [],
                delay: 100
            },
            showAutocompleteOnFocus: true
        });

        $('#programmer_form').on('submit', function (event) {
            event.preventDefault();
            if ($.trim($('#name').val()).length == 0) {
                alert("Please Enter Your Name");
                return false;
            } else if ($.trim($('#insta_us_name').val()).length == 0) {
                alert("Please Enter Atleast one Skill");
                return false;
            } else {
                var form_data = $(this).serialize();
                $('#submit').attr("disabled", "disabled");
                $.ajax({
                    url: "/instabotmv/store-new-task",
                    method: "POST",
                    data: form_data,
                    beforeSend: function () {
                        $('#submit').val('Submitting...');
                    },
                    success: function (data) {
                        if (data != '') {
                            $('#name').val('');
                            $('#insta_us_name').tokenfield('setTokens', []);
                            $('#success_message').html(data);
                            $('#submit').attr("disabled", false);
                            $('#submit').val('Submit');
                        }
                    }
                });
                setInterval(function () {
                    $('#success_message').html('');
                }, 5000);
            }
        });
  }); // end of document ready
})(jQuery); // end of jQuery name space





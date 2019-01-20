(function($){
  $(function(){

    $('#insta_tag').tokenfield({
            autocomplete: {
                source: ['People usign the most popular tags', 'Selfie,Handsome, Beautifull','Photographers, designers and artist','Fitness and workout lovers', 'Fashion people', 'hipster','Foodie','Travalers','Spiritual people','skaters and Surfers','Tattos and piercing lovers','Hair stylist and makeup artist','Couples and family people','Friends and party people','Geeks and apps user','Snapchat users', 'kik users', 'iPhone users', 'iPad users','android users', 'gamers','music lovers', 'movie lovers','cat lovers', 'bikers', 'dancers','girls', 'guys'],
                delay: 100
            },
            showAutocompleteOnFocus: true
        });


  }); // end of document ready
})(jQuery); // end of jQuery name space





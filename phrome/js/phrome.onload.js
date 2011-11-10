(function(){
    // Logging out of gmail takes you to a page where you have to click a
    // button to get back to a login form. Just go straight to that login
    if(window.location.href.toLowerCase() === 'http://www.google.com/mail/help/logout.html'){
        window.location.href = 'http://mail.google.com';
    }
}());

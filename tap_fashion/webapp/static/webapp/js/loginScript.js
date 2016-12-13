function readCookie(name) {
    name += '=';
    for (var ca = document.cookie.split(/;\s*/), i = ca.length - 1; i >= 0; i--) {
        if (!ca[i].indexOf(name)) {
            return ca[i].replace(name, '');
        }
    }
}

function initialize() {
    var testName = readCookie("username");
    document.getElementById('Name').innerHTML = 'Hello, ' + testName + '!';
}

function statusChangeCallback(response) {
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
        //Display his name
        initialize();
        //Display the body which we had hidden
        $('body').css('display', 'block');
    } else if (response.status === 'not_authorized') {
        document.cookie = "username=;";
        document.cookie = "userid=;";
        // The person is logged into Facebook, but not your app.
        window.location.href = "/webapp/";
    } else {
        document.cookie = "username=;";
        document.cookie = "userid=;";
        // The person is not logged into Facebook, so we're not sure if
        // they are logged into this app or not.
        window.location.href = "/webapp/";
    }
}

window.fbAsyncInit = function () {
     FB.init({
            appId: '338437033198950',
            cookie: true,  // enable cookies to allow the server to access
                           // the session
            xfbml: true,  // parse social plugins on this page
            version: 'v2.8' // use graph api version 2.5
        });
    // Now that we've initialized the JavaScript SDK, we call
    // FB.getLoginStatus().  This function gets the state of the
    // person visiting this page and can return one of three states to
    // the callback you provide.  They can be:
    //
    // 1. Logged into your app ('connected')
    // 2. Logged into Facebook, but not your app ('not_authorized')
    // 3. Not logged into Facebook and can't tell if they are logged into
    //    your app or not.
    //
    // These three cases are handled in the callback function.

    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
};

// Load the SDK asynchronously
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

function facebooklogout() {
    //call FB.logout() to logout the user
    //Note:
    // 1. If the user log into facebook from your app and
    // then presses logout, it will log out from facebook as welll
    // 2. If the user logs into facebook, and then into you app
    // the logout will only make him logout from the app
    FB.logout(function (response) {
        // user is now logged out
        FB.getLoginStatus(function (response) {
            statusChangeCallback(response);
        });
    });
}

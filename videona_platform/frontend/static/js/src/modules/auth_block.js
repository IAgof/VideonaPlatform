import React from 'react'
import RaisedButton from 'material-ui/lib/raised-button';
import FlatButton from 'material-ui/lib/flat-button'

import ThemeManager from 'material-ui/lib/styles/theme-manager';
import VideonaRawTheme from '../material_theme';


var SignupButton = React.createClass({
    //the key passed through context must be called "muiTheme"
    childContextTypes: {
        muiTheme: React.PropTypes.object,
    },

    getChildContext: function() {
        return {
            muiTheme: ThemeManager.getMuiTheme(VideonaRawTheme),
        };
    },

    render: function()  {
        return (
            <RaisedButton label="Signup" href="/" hoverColor="#ddd" className="signup-button" primary="true" />
        );
    }
});

var LoginButton = React.createClass({
    render: function() {
    return (<FlatButton label="Login" href="/login" className="login-button" hoverColor="#ddd" secondary="true" />)
    }
    })



const UserButtonsContainer = () => (
    <div className="navbar-login-buttons__container">
        <SignupButton />
        <div className="login-button-container"><LoginButton /></div>
    </div>
);

export default UserButtonsContainer;
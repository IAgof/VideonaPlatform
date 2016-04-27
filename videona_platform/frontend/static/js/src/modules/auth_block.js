import React from 'react'
import RaisedButton from 'material-ui/lib/raised-button';
import FlatButton from 'material-ui/lib/flat-button'

import ThemeManager from 'material-ui/lib/styles/theme-manager';
import VideonaRawTheme from '../material_theme';


class SignupButton extends React.Component {
    getChildContext() {
        return {
            muiTheme: ThemeManager.getMuiTheme(VideonaRawTheme)
        };
    }

    render()  {
        return (
            <RaisedButton label="Signup" href="/" hoverColor="#ddd" className="signup-button" primary="true" />
        );
    }
};

//the key passed through context must be called "muiTheme"
SignupButton.childContextTypes = {
    muiTheme: React.PropTypes.object
};


class LoginButton extends React.Component {
    render() {
        return (<FlatButton label="Login" href="/login" className="login-button" hoverColor="#ddd" secondary="true" />)
    }
}



const UserButtonsContainer = () => (
    <div className="navbar-login-buttons__container">
        <SignupButton />
        <div className="login-button-container"><LoginButton /></div>
    </div>
);

export default UserButtonsContainer;
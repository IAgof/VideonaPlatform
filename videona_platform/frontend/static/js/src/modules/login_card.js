import React from 'react'
import Dialog from 'material-ui/lib/dialog'
import TextField from 'material-ui/lib/text-field'
import RaisedButton from 'material-ui/lib/raised-button'
import FlatButton from 'material-ui/lib/flat-button'


class LoginDialog extends React.Component {
    constructor(props) {
        super(props)
        this.handleOpen = this.handleOpen.bind(this)
        this.handleClose = this.handleClose.bind(this)
        this.state = {
            open: false,
        }
    }

    handleOpen() {
        console.log('open handled!')
        this.setState({open: true})
    }

    handleClose() {
        this.setState({open: false})
    }


    render() {
        return (
            <div>
                <RaisedButton label="Signup" onTouchTap={this.handleOpen} hoverColor="#ddd"
                    className="signup-button" primary={true} />
                <FlatButton label="Login" onTouchTap={this.handleOpen} hoverColor="#ddd"
                    className="login-button" secondary={true}  />
                <Dialog modal={false} className="login-dialog"
                        open={this.state.open} onRequestClose={this.handleClose} >
                    <div className="logo videona-logo-md"></div>
                    <div>Please sign into your Videona account</div>
                    <LoginForm />
                </Dialog>
            </div>
        )
    }
}



class LoginForm extends React.Component {
    constructor() {
        super()
        this.handleUsernameChange = this.handleUsernameChange.bind(this)
        this.handlePasswordChange = this.handlePasswordChange.bind(this)
        this.state = { username: '', password: ''}
    }

    handleUsernameChange(e) {
        this.setState({username: e.target.value})
    }

    handlePasswordChange(e) {
        this.setState({password: e.target.value})
    }

    handleSubmit(e) {
        e.preventDefault()
        var username = this.state.username.trim();
        var password = this.state.password.trim();
        var csrftoken = $('meta[name=csrf-token]').attr('content')
        var data = {email: username, password: password, csrf_token: csrftoken}
//        if (!text || !author) {
//          return;
//        }
        $.ajax({
//            url: this.props.url,
            url: 'api/v1/auth',
            contentType: "application/json",
            dataType: 'json',
            type: 'POST',
            data: JSON.stringify(data),
//            beforeSend: function(xhr, settings) {
//                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
//                    xhr.setRequestHeader("X-CSRFToken", csrftoken)
//                }
//            }.bind(this),
            success: function(data) {
                console.log('/login SUCCESS', data)
                this.setState({data: data});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error(url, ' ', status, ' - ', err.toString());
            }.bind(this)
        });
//        this.setState({author: '', text: ''});
    }


    render() {
        return (
            <form className="commentForm" onSubmit={this.handleSubmit.bind(this)}>
                <TextField hintText="Username" className="login-form__username"
                    style={{ width: "100%" }}
                    value={this.state.username} onChange={this.handleUsernameChange} />
                <TextField hintText="Password" className="login-form__password" type="password"
                    style={{ width: "100%" }}
                    value={this.state.password} onChange={this.handlePasswordChange} />
                <RaisedButton label="Login" href="/login" className="login-form__login-button"
                    hoverColor="#ddd" secondary="true" onTouchTap={this.handleSubmit.bind(this)} />
            </form>
        )
    }
}

export default LoginDialog;
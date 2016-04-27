import React from 'react'
import Card from 'material-ui/lib/card/card'
import CardHeader from 'material-ui/lib/card/card-header'
import CardText from 'material-ui/lib/card/card-text'
import TextField from 'material-ui/lib/text-field'
import RaisedButton from 'material-ui/lib/raised-button';
import FlatButton from 'material-ui/lib/flat-button'

class LoginCard extends React.Component {
    render() {
        return (
            <Card className="login-card">
                <CardHeader title="Videona"
                    subtitle="Please sign into your Videona account." />
                <LoginForm />
           </Card>
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

    render() {
        return (
            <div>
                <TextField hintText="Username" className="login-card__username"
                value={this.state.username} onChange={this.handleUsernameChange} />
                <TextField hintText="Password" className="login-card__password" type="password"
                value={this.state.password} onChange={this.handlePasswordChange} />
                <RaisedButton label="Login" href="/login" className="login-card__login-button" hoverColor="#ddd" secondary="true" />
            </div>
        )
    }
}

export default LoginCard;
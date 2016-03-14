import injectTapEventPlugin from 'react-tap-event-plugin';

// Needed for onTouchTap
// Can go away when react 1.0 release
// Check this repo:
// https://github.com/zilverline/react-tap-event-plugin
injectTapEventPlugin();

// Basic React component that renders a Material-UI
// raised button with the text "Default"
import React from 'react'
import ReactDOM from 'react'
import ReactDriveIn from 'react-drive-in';
import RaisedButton from 'material-ui/lib/raised-button';
import FlatButton from 'material-ui/lib/flat-button'
import TextField from 'material-ui/lib/text-field'

const SignupButton = () => (
  <RaisedButton label="Signup" href="/" hoverColor="#ddd" primary="true" />
);

const LoginButton = () => (
  <FlatButton label="Login" href="/login" hoverColor="#ddd" secondary="true" />
);

const UserButtonsContainer = () => (
    <div class="navbar-login-buttons__container">
        <SignupButton /> <LoginButton />
    </div>
);

const SearchField = () => (
    <TextField
        hintText="Search"
        className="search-form-container__search"
        hintStyle={{
            color: '#fff'
        }}
        inputStyle={{
            color: '#fff'
        }}/>
);



const PLAYLIST_AWS = [
    [ "https://s3.amazonaws.com/tiedots/clips/VID_20160303_182238.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/VID_20160303_182251.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_000134.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/VID_20160303_182336.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/VID_20160303_182311.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181002.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181254.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181403.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181755.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_182114.mp4", ],
    [ "https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160310_163353.mp4", ],
];

const PLAYLIST_LOCAL = [
    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182238.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182251.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_000134.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182336.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182311.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181002.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181254.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181403.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181755.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_182114.mp4", ],
    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160310_163353.mp4", ],
];

var playlist_local = PLAYLIST_LOCAL

const VideoExploreBackground = () => (
    <ReactDriveIn
        showPlaylist={playlist_local}
        poster="https://v.cdn.vine.co/r/videos/BC1E72F54B1162065918138945536_334a62eeb04.1.4.13857093735400334228.mp4.jpg?versionId=1UnOMXNrM.LUbruTLS7no74m63ee4yYF"
    />
    );

export default SignupButton;

const loadedStates = ['complete', 'loaded', 'interactive'];
if (loadedStates.includes(document.readyState) && document.body) {
  run();
} else {
  window.addEventListener('DOMContentLoaded', run, false);
}

function run() {
    ReactDOM.render(<UserButtonsContainer />, document.getElementsByClassName('navigation-bar__auth-block')[0]);
    ReactDOM.render(<SearchField />, document.getElementsByClassName('search-form-container')[0]);
    ReactDOM.render(<VideoExploreBackground />, document.getElementsByClassName('explore-header__video-container')[0]);

}

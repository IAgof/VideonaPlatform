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
import TextField from 'material-ui/lib/text-field'

import VideoCard from './modules/video_card'
import LoginCard from './modules/login_card'
import LoginDialog from './modules/login_card'



const SearchField = () => (
    <TextField
        hintText="Search"
        className="search-form-container__search"
        hintStyle={{
            color: '#fff'
        }}
        inputStyle={{
            color: '#fff'
        }}
        style={{
            width: "100%"
        }}
        />
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

const HEADER_SLIDER = [ "http://videona.com/wp-content/uploads/2016/06/head-web.jpg",
    "http://videona.com/wp-content/uploads/2016/06/head-web-2.jpg",
    "http://videona.com/wp-content/uploads/2016/06/head-web-3.jpg",
    "http://videona.com/wp-content/uploads/2016/06/head-web-4.jpg" ]

//const PLAYLIST_LOCAL = [
//    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182238.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182251.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_000134.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182336.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/VID_20160303_182311.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181002.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181254.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181403.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_181755.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160303_182114.mp4", ],
//    [ "http://localhost:8000/frontend/static/img/clips/V_EDIT_20160310_163353.mp4", ],
//];

//var playlist_local = PLAYLIST_LOCAL
var playlist = PLAYLIST_AWS

const VideoExploreBackground = () => (
    <ReactDriveIn
        showPlaylist={playlist}
        poster="https://v.cdn.vine.co/r/videos/BC1E72F54B1162065918138945536_334a62eeb04.1.4.13857093735400334228.mp4.jpg?versionId=1UnOMXNrM.LUbruTLS7no74m63ee4yYF"
    />
    );

const VideoExplore = () => (
    <div className="video_explore">
        <VideoCard video_name="Video de aqui" video_file="https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160310_163353.mp4" />
        <VideoCard video_name="Vide o dos" video_file="https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181755.mp4" />
        <VideoCard video_name="O video del mamoor" video_file="https://s3.amazonaws.com/tiedots/clips/V_EDIT_20160303_181254.mp4" />
        {/*
        */}
    </div>
);

const loadedStates = ['complete', 'loaded', 'interactive'];
if (loadedStates.includes(document.readyState) && document.body) {
  run();
} else {
  window.addEventListener('DOMContentLoaded', run, false);
}

function run() {
    var auth_block = $('.navigation-bar__auth-block')[0]
    ReactDOM.render(<SearchField />, $('.search-form-container')[0]);
    ReactDOM.render(<VideoExploreBackground />, $('.explore-header__video-container')[0]);
    ReactDOM.render(<VideoExplore />, $('.article-content')[0])
    ReactDOM.render(<LoginDialog />, auth_block)
}

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
import RaisedButton from 'material-ui/lib/raised-button';

const MyAwesomeReactComponent = () => (
  <RaisedButton label="Default" href="/" />
);

export default MyAwesomeReactComponent;

const loadedStates = ['complete', 'loaded', 'interactive'];
if (loadedStates.includes(document.readyState) && document.body) {
  run();
} else {
  window.addEventListener('DOMContentLoaded', run, false);
}

function run() {
    ReactDOM.render(<MyAwesomeReactComponent />, document.getElementById('mount-point'));
}

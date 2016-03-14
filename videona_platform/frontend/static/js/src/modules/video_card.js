import React from 'react';
import Card from 'material-ui/lib/card/card';
import CardActions from 'material-ui/lib/card/card-actions';
import CardHeader from 'material-ui/lib/card/card-header';
import CardMedia from 'material-ui/lib/card/card-media';
import CardTitle from 'material-ui/lib/card/card-title';
import FlatButton from 'material-ui/lib/flat-button';
import CardText from 'material-ui/lib/card/card-text';
import ReactDriveIn from 'react-drive-in';


var VideoCard = React.createClass({
  render: function() {
    return (
        <Card className="video-card">
            <CardHeader className="video-card__header"
                title={this.props.video_name}
                subtitle="Video recorded the other day when we were young y tal..."
                avatar="http://lorempixel.com/100/100/nature/"
            />
            <CardMedia className="video-card__media"
                overlay={<CardTitle title="Overlay title" subtitle="Overlay subtitle" />}
            >
                <ReactDriveIn className="video-container"
                    show={this.props.video_file}
                    poster="http://raw.githubusercontent.com/ronik-design/react-drive-in/master/example/glacier.jpg"
                    paused={true}
                />
                <img src="http://lorempixel.com/600/337/nature/" />
            </CardMedia>
            <CardActions className="video-card__actions">
                <FlatButton label="Comments" />
                <FlatButton label="Pin it" />
            </CardActions>
        </Card>
    );
  }
});


export default VideoCard;
var Tabs = ReactBootstrap.Tabs;
var Tab = ReactBootstrap.Tab;
var ButtonToolbar = ReactBootstrap.ButtonToolbar;
var Button = ReactBootstrap.Button;
var Input = ReactBootstrap.Input;

function play(audio, times, ended) {
    if (times <= 0) {
	return;
    }
    var played = 0;
    audio.addEventListener("ended", function() {
	played++;
	if (played < times) {
	    audio.play();
	} else if (ended) {
	    ended();
	}
    });
    audio.play();
}

var AudioButton = React.createClass({
    getInitialState: function() {
	return {url: undefined,
		repeat: 1};
    },
    play: function() {
	var audio = new Audio(this.props.url);
	play(audio, this.props.repeat);
    },
    componentDidMount: function() {
    },
    render: function() {
	return(<Button bsStyle="success" onClick={this.play}>{this.props.text}</Button>);
    }
});

var HelloMessage = React.createClass({
    render: function() {
	return <div>Hello {this.props.name}</div>;
    }
});

var LogBox = React.createClass( {
    getInitialState: function() {
	return {data: "HelloWorld\n"};
    },
    addData: function (data) {
	var log = this.state.data;
	this.setState({data: log + data.level + ": " + data.msg + "\n"});
    },
    componentDidMount: function() {
	var source = new EventSource(this.props.url);
	var obj = this;
	source.addEventListener(this.props.event, function(event) {
	    var data = JSON.parse(event.data);
	    obj.addData(data);
	});
    },
    render: function() {
	return (<Input type="textarea" value={this.state.data} />);
    }
});

var Injector = React.createClass( {
    mixins: [React.addons.LinkedStateMixin],
    getInitialState: function() {
	return {message: 'Hello!'};
    },
    injectData : function() {
	$http.post("/inject-data",
		   JSON.parse($scope.textinput),
		   {"headers": {
		       "context-type" :
		       "application/json"}}).success(function (response) {
			   $scope.result = "done";
		       });
    },
    injectCtrl: function() {
	$http.post("/inject-control",
		   JSON.parse($scope.textinput),
		   {"headers": {"context-type" :
				"application/json"}}).success(function (response) {
				    $scope.result = "done";
				});
    },
    injectTest: function() {
	this.setState({message : "foo"});
    },
    fileOpen: function(e) {
	var self = this;
	var files = e.target.files,
	    reader = new FileReader();
	reader.onload = function() {
	    self.setState({input: this.result});
	}
	reader.readAsText(files[0]);
    },
    render: function() {
	return (
<div>
<Button bsStyle="success" onClick={this.injectTest}>Test</Button>
<Input type="file" onChange={this.fileOpen} />
<Input type="textarea" valueLink={this.linkState('input')} />
<Input type="textarea" valueLink={this.linkState('message')} />
</div>
	);
    }
});

function publish() {
    $.get("/publish-test");
};

const tabsInstance = (
<Tabs defaultActiveKey={2}>
    <Tab eventKey={1} title="Injector"><Injector/></Tab>
    <Tab eventKey={2} title="Tab 2"><HelloMessage name="John" /></Tab>
    <Tab eventKey={3} title="Tab 3">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>
	<AudioButton url="/static/high.ogg" repeat="3" text="High"/>
	<LogBox url="/subscribe" event="log" />
      </ButtonToolbar>
    </Tab>
</Tabs>
);

var helloWorld = React.createClass({
    render: function() {
	return (<h2>Greetings, from Real Python!</h2>)
    }
});

React.render(
    React.createElement(helloWorld, null),
    document.getElementById('content')
);
React.render(tabsInstance, document.getElementById('test'));

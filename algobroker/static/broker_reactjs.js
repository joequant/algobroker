var Tabs = ReactBootstrap.Tabs;
var Tab = ReactBootstrap.Tab;
var ButtonToolbar = ReactBootstrap.ButtonToolbar;
var Button = ReactBootstrap.Button;
var Input = ReactBootstrap.Input;

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

function publish() {
    $.get("/publish-test");
};

const tabsInstance = (
<Tabs defaultActiveKey={2}>
    <Tab eventKey={1} title="Tab 1">Hello</Tab>
    <Tab eventKey={2} title="Tab 2"><HelloMessage name="John" /></Tab>
    <Tab eventKey={3} title="Tab 3">
      <ButtonToolbar>
	<Button bsStyle="success" onClick={publish}>Ping</Button>
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

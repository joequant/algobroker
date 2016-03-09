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


const tabsInstance = (
<Tabs defaultActiveKey={2}>
    <Tab eventKey={1} title="Tab 1"><helloWorld></helloWorld></Tab>
    <Tab eventKey={2} title="Tab 2"><HelloMessage name="John" /></Tab>
    <Tab eventKey={3} title="Tab 3">
      <ButtonToolbar>
	<Button bsStyle="success">Ping</Button>
	<Input type="textarea" />
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

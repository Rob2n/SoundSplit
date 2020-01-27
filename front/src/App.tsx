import React from "react";
import { Layout } from "components/Layout";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Home } from "screens/Home";
import { Split } from "screens/Split";

const App: React.FC = () => {
	return (
		<Router>
			<Layout>
				<Switch>
					<Route exact path="/">
						<Home />
					</Route>
					<Route path="/split">
						<Split />
					</Route>
					<Route path="/faq"></Route>
				</Switch>
			</Layout>
		</Router>
	);
};

export default App;

import React from "react";
import { Link, Route } from "react-router-dom";
import "./MenuStyle.css";

const ListItemLink: React.FC<any> = ({ to, ...rest }) => {
	return (
		<Route
			path={to}
			exact
			children={({ match }) => (
				<li className={match ? "active" : ""}>
					<Link to={to} {...rest} />
				</li>
			)}
		/>
	);
};

const Menu: React.FC = () => {
	return (
		<div id="cssmenu">
			<ul>
				<ListItemLink to="/">Home</ListItemLink>
				<ListItemLink to="/split">Split</ListItemLink>
				<ListItemLink to="/faq">FAQs</ListItemLink>
			</ul>
		</div>
	);
};

export { Menu };

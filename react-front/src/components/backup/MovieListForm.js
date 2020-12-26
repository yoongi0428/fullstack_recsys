import React from 'react'
import { Button, List} from 'semantic-ui-react'

// // /* List with handle ver. */
// export default class MovieList extends Component {
// 	constructor(props) {
// 		this.state = {
// 			allMovies: [],
// 		};
// 	}
// 	state = {
// 		allMovies: [],
// 		selected: []
// 	}

// 	// add selected item into selected
// 	handleSelect = () =>
// 		this.setState((prevState) => ({
// 			allMovies: prevState.allMovies,
// 			selected: prevState.selected
// 		}))
	
// 	// clear selected items
// 	// handleClear = ()
// }

// callback을 App.js에서 만들고 넘겨줘서 button에서는 id만 넘겨준다.
// 리스트는 prop로 받은 movies만 항상 렌더링하도록 한다
// App.js는 id를 받아 리스트에서 다른 리스트로 옮겨서 state를 update한다
export const MovieList = ( { movies, Height}) => {
return (
	<List divided verticalAlign='middle' style={{overflow:'auto', maxHeight: Height}}>
	{movies.map(movie => {
		return (
		<List.Item key={movie.id}>
			<List.Content floated='right'>
				<Button> Select </Button>
			</List.Content>
			<List.Content>
				<List.Header as='a'>{movie.title}</List.Header>
				<List.Description as='a'>{movie.genre} / {movie.date} </List.Description>
			</List.Content>
			
			{/* <List.Content>{movie.title} / {movie.genre} / {movie.date} </List.Content> */}
		</List.Item>
		)
	})}
	</List>
)
}

// // /* Naive List ver. */
// export const MovieList = ( { movies, Height}) => {
// return (
// 	<List divided verticalAlign='middle' style={{overflow:'auto', maxHeight: Height}}>
// 	{movies.map(movie => {
// 		return (
// 		<List.Item key={movie.id}>
// 			<List.Content floated='right'>
// 				<Button> Select </Button>
// 			</List.Content>
// 			<List.Content>
// 				<List.Header as='a'>{movie.title}</List.Header>
// 				<List.Description as='a'>{movie.genre} / {movie.date} </List.Description>
// 			</List.Content>
			
// 			{/* <List.Content>{movie.title} / {movie.genre} / {movie.date} </List.Content> */}
// 		</List.Item>
// 		)
// 	})}
// 	</List>
// )
// }



// /* Table ver. */
// export const MovieList = ( { movies, Height }) => {
// 	return (
// 		<Table textAlign="center" color="blue" as={List} style={{overflow:'auto', maxHeight: Height}} compact celled definition >
// 		<Table.Header>
// 		<Table.Row>
// 			<Table.HeaderCell width={1} />
// 			<Table.HeaderCell width={8}> Title </Table.HeaderCell>
// 			<Table.HeaderCell width={5}> Genre </Table.HeaderCell>
// 			<Table.HeaderCell width={3}> Date</Table.HeaderCell>
// 		</Table.Row>
// 		</Table.Header>

// 		<Table.Body>
// 		{movies.map(movie => {
// 		return (
// 		<Table.Row key={movie.id} >
// 			<Table.Cell collapsing><Checkbox /></Table.Cell>
// 			<Table.Cell> {movie.title} </Table.Cell>
// 			<Table.Cell> {movie.genre} </Table.Cell>
// 			<Table.Cell> {movie.date} </Table.Cell>
// 			{/* <Image avatar src='https://react.semantic-ui.com/images/avatar/small/lena.png' /> */}
// 		</Table.Row>
// 		)
// 	})}
// 		</Table.Body>
// 	</Table>
// 	)
// 	}
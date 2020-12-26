import React from 'react';
import { List, Icon } from 'semantic-ui-react'

/* 
props
    - fullMovies: list of full movie object from DB
    - srcMovies: list of movies to show
    - tarMovies: list of movies to ad

*/

class RecommendList extends React.Component {    
    render() {
        return (
            
            <List divided verticalAlign='middle' style={{overflow:'auto', maxHeight: this.props.height}}>
            {this.props.recommendMovies.map(movie => {
                return (
                <List.Item
                    key={movie.id}
                    title={movie.title}
                    genre={movie.genre}
                    date={movie.date}>
                    <List.Content floated='left'>
                        {/* <Icon onClick={() => this.props.onEvent(movie)} content={'Info'} />  */}
                        <Icon circular name='heart' color='red' />
                    </List.Content>
                    <List.Content>
                        <List.Header as='a'>{movie.title}</List.Header>
                        <List.Description as='a'>{movie.genre} / {movie.date} </List.Description>
                    </List.Content>
                </List.Item>
                )
            })}
            </List>
        );
    }
}
export default RecommendList;
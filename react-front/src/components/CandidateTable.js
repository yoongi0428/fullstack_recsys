import React from 'react';
import { Button, Table } from 'semantic-ui-react'

/* 
props
    - fullMovies: list of full movie object from DB
    - srcMovies: list of movies to show
    - tarMovies: list of movies to ad

*/

class CandidateTable extends React.Component {    
    render() {
        return (
            // verticalAlign='middle'
            <div class="scrolling content" style={{overflow:'auto', maxHeight: this.props.height}}>
            <Table sortable compact celled definition textAlign="center">
                <Table.Header>
                    <Table.Row>
                        <Table.HeaderCell />
                        <Table.HeaderCell>Title</Table.HeaderCell>
                        <Table.HeaderCell>Genre</Table.HeaderCell>
                        <Table.HeaderCell>Date</Table.HeaderCell>
                    </Table.Row>
                </Table.Header>
                <Table.Body>
                {this.props.candidateMovies.map(movie => {
                    return (
                        <Table.Row>
                            <Table.Cell collapsing width="1">
                            <Button 
                            inverted
                            active={this.props.candidateMovies.includes(movie)}
                            color='olive'
                            onClick={() => this.props.onEvent(movie)}
                            content='Add' />
                            </Table.Cell>
                            <Table.Cell width="6">{movie.title}</Table.Cell>
                            <Table.Cell width="4">{movie.genre}</Table.Cell>
                            <Table.Cell width="2">{movie.date}</Table.Cell>
                        </Table.Row>)
                })}
                </Table.Body>
            </Table>
            </div>
        );
    }
}
export default CandidateTable;
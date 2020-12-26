import React from 'react';
import { Button, Table } from 'semantic-ui-react'

class ContextTable extends React.Component {    
    render() {
        return (
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
                {this.props.contextMovies.map(movie => {
                    return (
                        <Table.Row>
                            <Table.Cell collapsing width="1">
                            <Button 
                                inverted
                                color='olive'
                                onClick={() => this.props.onEvent(movie)}
                                content={'Delete'} /> 
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
export default ContextTable;
import React from 'react';
import { Icon, Table } from 'semantic-ui-react'

class RecommendTable extends React.Component {    
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
                {this.props.recommendMovies.map(movie => {
                    return (
                        <Table.Row>
                            <Table.Cell collapsing width="1">
                            <Icon circular name='heart' color='red' />
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
export default RecommendTable;
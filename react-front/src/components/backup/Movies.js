import React from 'react';
import { List, Header } from 'semantic-ui-react';

export const Movies = ( { movies } ) => {
    return (
        <List>
            {movies.map(movie => {
                return (
                <List.Item key={movie.id}>
                    <Header>{movie.title}</Header>
                </List.Item>
            )
            })}
        </List>
        // <div>{movies.length}</div>
    );
}
import React, {useState} from 'react';
import { Button, Form, Input } from 'semantic-ui-react';

export const MovieForm = ({onNewMovie}) => {
    const [title, setTitle] = useState('');

    return (
        <Form>
            <Form.Field>
                <Input 
                    placeholder='movie title'
                    value={title}
                    onChange={e => setTitle(e.target.value)}
                />
            </Form.Field>
            <Form.Field>
                <Button onClick={async () => {
                    // const response = await fetch('', {
                    //     method: 'POST',
                    //     headers: {
                    //         'Content-Type': 'application.json'
                    //     },
                    //     body: JSON.stringify()
                    // })
                    // if (response.ok) {
                    //     console.log('response worked!');
                    // }
                    console.log('response worked!');
                    onNewMovie({'id': 111, 'title': 'test', 'genre': 'test'})
                }}> Submit </Button>

            </Form.Field> 
        </Form>
    )
}
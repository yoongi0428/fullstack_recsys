import React from 'react'
import { Button, Select, Input } from 'semantic-ui-react'

class SearchForm extends React.Component {
    options = [
        // { key: 'all', text: 'All', value: 'all' },
        { key: 'title', text: 'Title', value: 'title' },
        { key: 'genre', text: 'Genre', value: 'genre' },
    ]

    constructor(props){
        super(props);
        this.state = {searchValue: "asdf"}
    }

    render() {
        return (
        <Input type='text' placeholder='Search...' action>
            <input onChange={(e, data) => {this.setState({searchValue: e.target.value})}}/>
            <Select compact
                    options={[
                        // { key: 'all', text: 'All', value: 'all' },
                        { key: 'title', text: 'Title', value: 'title' },
                        { key: 'genre', text: 'Genre', value: 'genre' },
                    ]}
                    defaultValue={this.props.searchKey}
                    onChange={(e, data) => this.props.onSelectChange(e, data)}/>
            <Button type='submit' onClick={() => this.props.onSearchClick(this.props.searchKey, this.state.searchValue)}>Search</Button>
        </Input>
    )}
}

export default SearchForm;
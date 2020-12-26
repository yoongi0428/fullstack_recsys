import React from "react";
import { Search } from "semantic-ui-react";
import _ from "lodash";

class SearchBox extends React.Component {
    state = {
        isLoading: false,
        results: [],
        value: ""
    };

    componentWillMount() {
        this.resetComponent();
    }

    resetComponent = () =>
        this.setState({ isLoading: false, results: [], value: "" });

    handleSearchChange = (e, { value }) => {
        this.setState({ isLoading: false, value });

        // setTimeout(() => {
        //     if (this.state.value.length < 1) this.resetComponent();

        //     const re = new RegExp(_.escapeRegExp(this.state.value), "i");
        //     const isMatch = result => re.test(result.title);

        //     this.setState({
        //         isLoading: false,
        //         results: _.filter(this.props.movies, isMatch)
        //     });
        // }, 500);
    };

    handleResultSelect = (e, { result }) =>
        this.setState({ value: result.title });

    render() {
        const { isLoading, results, value } = this.state;
        return (
            <div>
                <Search
                    type="text"
                    size="big"
                    loading={isLoading}
                    results={results}
                    value={value}
                    onSearchChange={this.handleSearchChange}
                    // onResultSelect={this.handleResultSelect}
                    showNoResults={false}
                />
            </div>
        );
    }
}

export default SearchBox;
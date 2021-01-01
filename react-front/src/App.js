import React from 'react';
// import logo from './logo.svg';
import './App.css';
import CandidateTable from './components/CandidateTable'
import ContextTable from './components/ContextTable'
import RecommendTable from './components/RecommendTable'
import SearchForm from './components/SearchForm'
import { Container, Icon, Button, Grid, Select } from "semantic-ui-react"
import _ from "lodash";

class App extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      fullMovies: [],
      candidates: [],
      candidatesShow: [],
      selected: [],
      recommended: [],
      searchKey: "title",
      searchValue: "",
      modelKey: "EASE"
    }
    this.loadMovieDB = this.loadMovieDB.bind(this);
    this.onRefreshClick = this.onRefreshClick.bind(this)
    this.onCandidateClick = this.onCandidateClick.bind(this)
    this.onSelectedClick = this.onSelectedClick.bind(this)
    this.onRecommendClick = this.onRecommendClick.bind(this)
    this.onSearchClick = this.onSearchClick.bind(this)
    this.onSearchChange = this.onSearchChange.bind(this)
    this.onSelectChange = this.onSelectChange.bind(this)
    this.onModelSelectClick = this.onModelSelectClick.bind(this)

    this.loadMovieDB();
  }

  loadMovieDB(){
    fetch('/init', {method: 'GET'}).then(response =>
      response.json().then(data => {this.setState((prevState) => ({
        fullMovies: data.result,
        candidates: data.result,
        candidatesShow: data.result,
        selected: prevState.selected,
        recommended: prevState.recommended
      }))}))
  }

  onRefreshClick(){
    this.setState((prevState) => ({
      fullMovies: prevState.fullMovies,
      candidates: prevState.fullMovies,
      candidatesShow: prevState.fullMovies,
      selected: [],
      recommended: []
    }))
  }

  onCandidateClick(movie){
    // check if movie already exists in candidates
    let alreadyExists = this.state.selected.includes(movie)
    if (!alreadyExists) {
      let movieIndex = this.state.candidatesShow.indexOf(movie);
      this.setState((prevState) => ({
        ...prevState,
        candidatesShow: [...prevState.candidatesShow.slice(0, movieIndex), ...prevState.candidatesShow.slice(movieIndex+1, prevState.candidatesShow.length)],
        selected: [...prevState.selected, movie],
      }))
    }
  }

  onSelectedClick(movie){
    let alreadyExists = this.state.selected.includes(movie)
    if (alreadyExists) {
      let movieIndex = this.state.selected.indexOf(movie);
      console.log(movieIndex);
      this.setState((prevState) => ({
          ...prevState,
          candidatesShow: [...prevState.candidatesShow, movie],
          selected: [...prevState.selected.slice(0, movieIndex), ...prevState.selected.slice(movieIndex+1, prevState.selected.length)],
        }))
    }
  }

  onSearchChange(e, data) {
    this.setState((prevState) => ({
      ...prevState,
      searchValue: e.target.value
    }))
  }

  onSelectChange(e, data) {
    this.setState((prevState) => ({
      ...prevState,
      searchKey: data.value
    }))
  }

  onSearchClick(type, query) {
    if (query.length < 1){
      this.setState((prevState) => ({
        ...prevState,
        candidatesShow: prevState.candidates
      }))
    }
    else {
      const re = new RegExp(_.escapeRegExp(query), "i");
      const isMatch = type === "title" ? result => re.test(result.title) : result => re.test(result.genre);
      const results = this.state.candidates.filter(isMatch).filter(data => this.state.candidatesShow.includes(data))
      this.setState((prevState) => ({
        ...prevState,
        candidatesShow: results
      }))
    }
  }
  onModelSelectClick(e, data){
    this.setState((prevState) => ({
      ...prevState,
      modelKey: data.value
    }))
  }
  
  onRecommendClick(){
    if (this.state.selected.length < 1){
      console.log('ZERO CONTEXT')
    }
    // gather ids from selected list
    let context_ids = this.state.selected.map(movie => movie.id);
    // call recommend api
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        context: context_ids,
        model: this.state.modelKey})
    };
    fetch('/recommend', requestOptions).then(response =>
      response.json().then(data => {this.setState((prevState) => ({
        fullMovies: prevState.fullMovies,
        candidates: prevState.candidates,
        selected: prevState.selected,
        recommended: data.result
      }))}))
  }

  render(){
    return (
      <div className="App">
        <header class="ui grid" style={{marginTop:40, paddingBottom: 100}}>
          <div style={{fontSize: "4rem", float: "left", width: "20%"}}>
              <Icon link onClick={this.onRefreshClick} name='home' />
          </div>
          <div style={{fontFamily: 'Impact, sans-serif', fontSize: "4rem", float: "left", width: "60%"}}> Recommender System Playground </div>
          <div style={{fontFamily: "Palatino Linotype, Book Antiqua, Palatino, serif", fontSize: "2rem", float: "left", width: "20%"}}>
            Yoonki Jeong
            <a href='https://github.com/yoongi0428'><Icon name='github' /></a>
            <a href='https://yoonki-j.info/'><Icon name='wordpress' /></a>
          </div>
        </header>
        {/* body */}
        <Container style={{width: "90%", marginTop: 40, paddingBottom: 50, textAlign: "center"}}>
          <Grid>
            <Grid.Row columns={2}>
              <Grid.Column>
                <SearchForm 
                  onSearchChange={this.onSearchChange}
                  onSearchClick={this.onSearchClick}
                  onSelectChange={this.onSelectChange}
                  searchKey={this.state.searchKey}>
                </SearchForm>
              </Grid.Column>
            </Grid.Row>
            <Grid.Row columns={2}>
              <Grid.Column>
                <CandidateTable 
                fullMovies={this.state.fullMovies} 
                candidateMovies={this.state.candidatesShow}
                selectedMovies={this.state.selected}
                onEvent={this.onCandidateClick}
                height={600}></CandidateTable>
              </Grid.Column>
              <Grid.Column>
                <ContextTable
                fullMovies={this.state.fullMovies} 
                contextMovies={this.state.selected}
                onEvent={this.onSelectedClick}
                height={600}></ContextTable>
              </Grid.Column>
            </Grid.Row>
            <Grid.Row></Grid.Row>
            <Grid.Row></Grid.Row>
          </Grid>
  
        </Container>
        {/* BUTTON: generate recommendation */}
        <div style={{textAlign: "center"}}>
          <Select compact
                  options={[
                      { key: 'ease', text: 'EASE', value: 'EASE' },
                      { key: 'itemknn', text: 'ItemKNN', value: 'ItemKNN' },
                  ]}
                  defaultValue={this.state.modelKey}
                  onChange={(e, data) => this.onModelSelectClick(e, data)}/>
          <Button icon labelPosition='left' onClick={this.onRecommendClick}><Icon circular name='fire' color='red' />RECOMMEND!</Button>
        </div>
        
  
        {/* Recommendation table */}
        <div style={{textAlign: "center"}}>
          <Container id="recommendation" style={{margin: "0 auto", paddingTop: 50, width: "40%", display: "inline-block", verticalAlign: "top"}}>
            {/* <MovieList movies={this.state.recommended} Height={500}/> */}
            <RecommendTable
              fullMovies={this.state.fullMovies} 
              recommendMovies={this.state.recommended}
              // onEvent={this.onSelectedClick}
              height={500}></RecommendTable>
          </Container>
        </div>
        <footer class="ui grid" style={{paddingTop: 50, margin: "0 auto", width: "80%", display: "inline-block", verticalAlign: "top"}}>
          <div style={{fontSize: "4rem", float: "left", width: "100%"}}>   </div>
        </footer>
      </div>
    );
  }
}

export default App;
// import React, { useEffect, useState } from 'react';
import React from 'react';
import logo from './logo.svg';
import './App.css';
import CandidateList from './components/CandidateList'
import ContextList from './components/ContextList'
import RecommendList from './components/RecommendList'
import CandidateTable from './components/CandidateTable'
import ContextTable from './components/ContextTable'
import RecommendTable from './components/RecommendTable'
import { Container, Icon, Button } from "semantic-ui-react"

class App extends React.Component {
  constructor(props){
    super(props);

    this.state = {
      fullMovies: [],
      candidates: [],
      selected: [],
      recommended: []
    }
    this.loadMovieDB = this.loadMovieDB.bind(this);
    this.onRefreshClick = this.onRefreshClick.bind(this)
    this.onCandidateClick = this.onCandidateClick.bind(this)
    this.onSelectedClick = this.onSelectedClick.bind(this)
    this.onRecommendClick = this.onRecommendClick.bind(this)

    this.loadMovieDB();
  }

  loadMovieDB(){
    fetch('/init', {method: 'GET'}).then(response =>
      response.json().then(data => {this.setState((prevState) => ({
        fullMovies: data.result,
        candidates: data.result,
        selected: prevState.selected,
        recommended: prevState.recommended
      }))}))
  }

  onRefreshClick(){
    this.setState((prevState) => ({
      fullMovies: prevState.fullMovies,
      candidates: prevState.fullMovies,
      selected: [],
      recommended: []
    }))
  }

  onCandidateClick(movie){
    // check if movie already exists in candidates
    let alreadyExists = this.state.selected.includes(movie)
    if (!alreadyExists) {
      let movieIndex = this.state.candidates.indexOf(movie);
      this.setState((prevState) => ({
        fullMovies: prevState.fullMovies,
        candidates: [...prevState.candidates.slice(0, movieIndex), ...prevState.candidates.slice(movieIndex+1, prevState.candidates.length)],
        selected: [...prevState.selected, movie],
        recommended: prevState.recommended
      }))
    }
  }

  onSelectedClick(movie){
    let alreadyExists = this.state.selected.includes(movie)
    if (alreadyExists) {
      let movieIndex = this.state.selected.indexOf(movie);
      console.log(movieIndex);
      this.setState((prevState) => ({
          fullMovies: prevState.fullMovies,
          candidates: [...prevState.candidates, movie],
          selected: [...prevState.selected.slice(0, movieIndex), ...prevState.selected.slice(movieIndex+1, prevState.selected.length)],
          recommended: prevState.recommended
        }))
    }
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
        model: 'EASE'})
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
          <div style={{fontSize: "2rem", float: "left", width: "20%"}} onClick={this.onRefreshClick}> HOME </div>
          <div style={{fontSize: "4rem", float: "left", width: "60%"}}> Full Stack RecSys </div>
          <div style={{fontSize: "2rem", float: "left", width: "20%"}}>
            Yoonki Jeong
            <a class="ui image label"><img src="/images/avatar/small/joe.jpg"/></a>
          </div>
        </header>
        <Container style={{width: "90%", marginTop: 40, paddingBottom: 50, textAlign: "center"}}>
          {/* Full movie table */}
          <Container id="full" style={{margin: "0 auto", width: "50%", display: "inline-block", verticalAlign: "top"}}>
              <CandidateTable 
              fullMovies={this.state.fullMovies} 
              candidateMovies={this.state.candidates}
              selectedMovies={this.state.selected}
              onEvent={this.onCandidateClick}
              height={600}></CandidateTable>
          </Container>
  
          {/* Context table */}
          <Container id="selected" style={{margin: "0 auto", width: "50%", display: "inline-block", verticalAlign: "top"}}>
            {/* <MovieList movies={this.state.candidates} Height={600}/> */}
            <ContextTable
              fullMovies={this.state.fullMovies} 
              contextMovies={this.state.selected}
              onEvent={this.onSelectedClick}
              height={600}></ContextTable>
          </Container>
  
        </Container>
        {/* BUTTON: generate recommendation */}
        <div style={{textAlign: "center"}}>
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
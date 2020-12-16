import React, { Component } from 'react';
import $ from 'jquery';

import '../stylesheets/FormView.css';

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
	  newcategory:""
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
	var message=document.getElementById('message1');
    $.ajax({
      url: '/newquestions', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
		  message.innerHTML="Question  Added with success !!!"
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        message.innerHTML="Question not Added please try again!!!"
        return;
      }
    })
  }
  
  /**/
  submitCategory = (event) => {
    event.preventDefault();
	var message=document.getElementById('message');
    $.ajax({
      url: '/newcategories', //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        category: this.state.newcategory,
        
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
		  //alert('new category added, please reload this page to show the new category in the select option')
		  
		  // get reference to select element
			var sel = document.getElementById('select');
			
			// create new option element
			var opt = document.createElement('option');

			// create text node to add to option element (opt)
			opt.appendChild( document.createTextNode(result.category.type) );

			// set value property of opt
			opt.value = result.category.id; 
			opt.key = result.category.id; 

			// add opt to end of select box (sel)
			sel.appendChild(opt); 
			message.innerHTML="Category Added with success"
			document.getElementById("add-question-form").reset();
		
        return;
      },
      error: (error) => {
        //alert('Unable to add question. Please try your request again')
        message.innerHTML="Category not Added !!!"
		return;
      }
    })
  }
  
  /**/

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
	<div>
      <div id="add-form">
        <h2>Add a New Trivia Question</h2>
        <form className="form-view" id="add-question-form" onSubmit={this.submitQuestion}>
          <label>
            Question
			</label>
            <input type="text" name="question" onChange={this.handleChange}/>
          
          <label>
            Answer
			 </label>
            <input type="text" name="answer" onChange={this.handleChange}/>
         
          <label>
            Difficulty
			 </label>
            <select name="difficulty" onChange={this.handleChange}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
            </select>
         
          <label>
            Category
			</label>
            <select id='select' name="category" onChange={this.handleChange}>
              {Object.keys(this.state.categories).map(id => {
                  return (
                    <option key={id} value={id}>{this.state.categories[id]}</option>
                  )
                })}
            </select>
          
          <input type="submit" className="button" value="Submit" />
		  <p id="message1">You can add  category</p>
        </form>
      </div>
	  
	  <div id="add-form-cat">
        <h2>Add a New Trivia Category</h2>
        <form className="form-view" id="add-category-form" onSubmit={this.submitCategory}>
          <label>
            Category
			</label>
            <input type="text" name="newcategory" onChange={this.handleChange}/>
          
          
          <input type="submit" className="button" value="Submit" />
		  <p id="message">You can add  category</p>
        </form>
      </div>
	  </div>
    );
  }
}

export default FormView;

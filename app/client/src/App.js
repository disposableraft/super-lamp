import React from 'react';
import axios from 'axios';
import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
    this.handleUpload = this.handleUpload.bind(this);
    this.handlePaste = this.handlePaste.bind(this);
    this.handleUploadChange = this.handleUploadChange.bind(this);
    this.handleURL = this.handleURL.bind(this);
    this.handleURLChange = this.handleURLChange.bind(this);
    this.toggleMode = this.toggleMode.bind(this);
    this.state = {
      image: '',
      predictions: [
        {name: null, pred: null},
        {name: null, pred: null},
        {name: null, pred: null}
      ],
      uploadMode: true,
    };
  }

  handleURL(event) {
    event.preventDefault();
    axios.get('http://localhost:5000/url', {
      params: {
        url: this.state.image
      }
    })
    .then((response) => {
      this.setState(state => {
        return {
          predictions: response.data.predictions,
        };
      })
    })
    .catch((error) => {
      console.error(error);
    })
  }

  handleUpload(event) {
    event.preventDefault();
    const url = 'http://localhost:5000/upload';
    const formData = new FormData();
    formData.append('file', this.fileInput.current.files[0]);
    axios({
      method: 'post',
      url: url,
      data: formData
    })
    .then(response => {
      this.setState(state => {
        return {
          predictions: response.data.predictions,
        };
      })
    })
    .catch(error => {
      console.error(error)
    });
  }

  handleURLChange(event) {
    this.setState(
      {
        image: event.target.value
      }
    )
  }

  handleUploadChange(event) {
    this.setState(
      { image: URL.createObjectURL(event.target.files[0]) }
    )
  }

  handlePaste(event) {
    event.preventDefault();
    navigator.clipboard.readText().then(text => {
      if (isImage(text)) {
        this.setState(
          {image: text}
        )
      } else {
        alert(`"${text}" is not a valid URL to a JPG.`)
      }
    });
  }

  toggleMode(event) {
    event.preventDefault();
    this.setState(state => {
      return {
        image: '',
        uploadMode: !state.uploadMode,
      };
    });
  }

  render() {
    const {
      image,
      predictions,
      uploadMode
  } = this.state;

    const uploadForm = (
      <form onSubmit={this.handleUpload} >
        <h3>Select image to upload:</h3>
        <input type="file" ref={this.fileInput} onChange={this.handleUploadChange} />
        <button type="submit">Classify</button>
      </form>
    );

    const urlForm = (
      <div>
        <h3>Enter a URL</h3>
          <form onSubmit={this.handleURL}>
            <button onClick={this.handlePaste}>paste</button> <input type="text" value={image} onChange={this.handleURLChange} disabled />
            <button type="submit">Classify</button>
          </form>
      </div>
    );

    return (
      <div className="App">
        <header className="App-header">
          {!predictions[0].name ? <h1>Dog Classifier</h1> : <h1>I bet that {format_probability(predictions[0].prob)}% this is a {predictions[0].name}!</h1>}
        </header>
        <div>
            {!uploadMode ? urlForm : uploadForm}
            <p>
              {!image ? null : <img height="500px" src={image} alt="hopefullyadog" />}
            </p>
            <p>OR</p>
            <button onClick={this.toggleMode}>{!uploadMode ? 'Upload Image' : 'Enter URL'}</button>
          </div>
      </div>
    );
  }
}

function isImage(string) {
  const re = new RegExp('^http.*jpg$');
  return re.test(string);
}

function format_probability(p) {
  return Math.round(p * 100)
}

export default App;

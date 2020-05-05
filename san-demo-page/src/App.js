import React from 'react';
import './App.css';
import { Placeholder, Container, Button, Header, Icon, Segment } from 'semantic-ui-react'
import $ from "jquery"
import arrow from './arrows.png';
import before from './before.jpg';
import after from './after.jpg';

var inputImageSrc = arrow;
var outputImageSrc;
var marginX;    // 外部宽度，即滑动区域左侧到浏览器边框的距离

const submitImage = (input) => {
  //Add logic here to make a http call to server and retrive the generated image
  var preview = $("#beforeImg")
  var file    = document.querySelector('input[type=file]').files[0];
  var reader  = new FileReader();

  reader.onloadend = function () {
    console.log("LOADED")
    preview.attr("src", reader.result)
  }

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = arrow;
  }
  fetchGeneratedResource(file)
};

const fetchGeneratedResource = (file) => {
  let fd = new FormData();
  fd.append("file", file);
  console.log(file)
  fetch('http://54.193.204.208:8080/uploadImage', {
    method: 'POST', // or 'PUT'
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*'
    },
    body: fd
  }).then((response)=> {
    return response.json()
  }).then(data => {
    console.log(data)
  })
}

const mockClick = (event) => {
  $("#file").click()
}


const mouseDownHander = (e) => {
  const slider = document.querySelector('.slider-wrap');    // 整个滑动区域
  const handler = document.querySelector('.handler'); 
  marginX = e.pageX - handler.offsetLeft;
  // envent.pageX : 点击时鼠标相对浏览器边框的 X 距离；
  // elenment.offsetLeft : 元素 left 属性值。
  // 此时，内框absolute，外框relative，所以 left 是相对外框的距离；
  slider.addEventListener('mousemove', moveHandler);
}

const onmouseUpHander = (e) => {
  const slider = document.querySelector('.slider-wrap');
  slider.removeEventListener('mousemove', moveHandler);
}

const moveHandler = (e) => {
  const beforeImg = document.querySelector('.before-img');  // 左边图片外框
  const handler = document.querySelector('.handler'); 
  handler.style.left = e.pageX - marginX + 'px';
  beforeImg.style.width = e.pageX - marginX + 'px';
  // 此时 e.pageX 是鼠标滑动时据浏览器左边的距离，减去外部距离，
  // 即得到此时鼠标相对于图片区域的 X 坐标；
  // 让滑动条的 left 和左边图片宽度 都等于坐标，即可以达到跟随效果；
}

const finishLoading = (e) => {
  const placeHolder = $("#placeHolder")
  const resultView = $("#resultView")
  placeHolder.hide()
  resultView.show()
}



function App() {
  setTimeout(()=> {
    finishLoading()
  }, 3000)
  return (
    <div className="App">
      <header className="App-header">
        <div className="uploadForm">
          <Segment className="segment">
            {/* <Header icon>
              <Icon name='pdf file outline' />
              Please upload an image
            </Header> */}

            <Button primary onClick={mockClick}>Upload Image</Button>
          </Segment>
        </div>

        {/* <div id="inputImg" className="InputImage" hidden>
            <img id="uploadImg" className="in-img" src={inputImageSrc} style={{width:"100%", objectFit: "contain"}}/>
        </div>
        <img id="arrow" className="arrow" src={arrow} alt="arrow" hidden/>
        <div id="genImg" className="generatedImage" hidden>
            {loading? (<Placeholder className="customMaxWidth">
              <Placeholder.Image square />
            </Placeholder>):(<img id="gImg" className="gen-image" src={outputImageSrc} style={{width:"100%", objectFit: "contain"}}/>)}
        </div> */}


      <div class="container">
        <Placeholder id="placeHolder" style={{width:document.documentElement.clientWidth, height:document.documentElement.clientHeight}} className="customMaxWidth">
          <Placeholder.Image />
        </Placeholder>
        <div id="resultView" class="slider-wrap" hidden>
          <div class="before-img">
            <img id="beforeImg" style={{width:document.documentElement.clientWidth}} class="preventDragging" src={before} alt=""/>
          </div>
          <img id="afterImg" style={{width:document.documentElement.clientWidth}}  class="preventDragging" src={after} alt=""/>
          <span class="handler" onMouseUp={onmouseUpHander} onMouseDown={mouseDownHander}></span>
        </div>
      </div>
      </header>
      <input type="file"  accept="image/*" name="image" id="file" onChange={submitImage} hidden></input>
    </div>
  );
}

export default App;

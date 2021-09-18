import React, { useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Divider, Button, ImageList, ImageListItem, ImageListItemBar, IconButton } from '@material-ui/core';
import { Input }  from '@mui/material';
import HighlightOffIcon from '@mui/icons-material/HighlightOff';

const useStyles = makeStyles((theme) => ({
  app:{
    textAlign: 'center',
    height: '95vh',
    display: 'block',
    overflow: 'auto',
  },
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
    height: '95%', 
    backgroundColor: theme.palette.background.paper,
  },
  imageList: {
    width: '800px',
    height: '100%',
    transform: 'translateZ(0)',
    '&::-webkit-scrollbar': {
      width: '0.4em'
    },
    '&::-webkit-scrollbar-track': {
      boxShadow: 'inset 0 0 6px rgba(0,0,0,0.00)',
      webkitBoxShadow: 'inset 0 0 6px rgba(0,0,0,0.00)'
    },
    '&::-webkit-scrollbar-thumb': {
      backgroundColor: 'rgba(0,0,0,.1)',
      outline: '1px solid slategrey'
    }
  },
  actions:{
    marginTop: '5px'
  },
  titleBar: {
    background:
      'linear-gradient(to bottom, rgba(0,0,0,0.7) 0%, ' +
      'rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)',
  },
  icon: {
    color: 'white',
  },
  search_name_input: {
    size: "small",
    marginLeft: '10px'
  }
}));

function App() {

  const classes = useStyles();

  const [Images, setImages] = useState([]);
  const [searchName, setSearchName] = useState(null)
  

  useEffect(() => {
    fetchImages().then(fetched_images => {
      setImages(fetched_images)
    })
  }, []);

  async function fetchImages() {
    const new_images = []
    const response = await fetch('http://localhost:5000/fetch', {
      mode: 'cors',
      headers: {
        'content-type': 'application/json'
      }
    })
    const response_json = await response.json()
    for(var i=0;i<response_json['images'].length;i++){
      const base64img = response_json['images'][i]
      const blob = await fetch(`data:${base64img.image_type};base64,${base64img.image_base64}`).then(res => res.blob())
      const image_file = new File([blob], base64img.image_name, {type: base64img.image_type,});
      new_images.push({
        'id': base64img.id,
        'image_name': base64img.image_name,
        'image_file': image_file
      })
    }
    return new_images
  }
  

  const addImages = (event) => {

    if (event.target.files) {
      let imgs_array = Array.from(event.target.files);
      let formData = new FormData();

      event.target.value=null
      imgs_array.forEach(img => formData.append('images', img));

      fetch('http://localhost:5000/upload', {
        mode: 'cors',
        method: "POST",
        body: formData,
      })
      .then(response => response.json())
      .then(response_json => {
        if (response_json['image_ids']){
          var upload_images = []
          const image_ids = response_json['image_ids']
          for(var i=0; i<image_ids.length; i++){
            
            upload_images.push({
              'id': image_ids[i],
              'image_name': imgs_array[i].name,
              'image_file': imgs_array[i]
            })
          }
          setImages([...Images, ...upload_images])
        }
      })

    }
  }

  const deleteImage = (id) => {
    fetch('http://localhost:5000/delete', {
        mode: 'cors',
        method: "POST",
        headers:{
          'content-type': 'application/json'
        },
        body: JSON.stringify({ids: [id]}),
    }).then(response=>{
      if(response.status === 200){
        setImages(Images.filter(e => e.id !== id))
      }
    })
  }
  
  return (
    <div className={classes.app}>
      <div className={classes.root}>
        <ImageList rowHeight={300} cols={3} gap={4} className={classes.imageList}>
        {Images.map((image) => (
          !searchName || image.image_name.includes(searchName)?
          <ImageListItem key={image.id} cols={1} rows={1}>
            <img src={image.image_file && URL.createObjectURL(image.image_file)} alt={image.image_name} />
            <ImageListItemBar
              title={image.image_name}
              position="top"
              actionIcon={
                <IconButton onClick={()=>{deleteImage(image.id)}} aria-label={`star ${image.image_name}`} className={classes.icon}>
                  <HighlightOffIcon/>
                </IconButton>
              }
              actionPosition="left"
              className={classes.titleBar}
            />
          </ImageListItem>:null
        ))}
      </ImageList>
      </div>
      <Divider  variant="middle"/>
      <div className = {classes.actions}>
        <input
          accept="image/*"
          style={{display: 'none'}}
          onChange={addImages}
          id="contained-button-file"
          multiple
          type="file"
        />
        <label htmlFor="contained-button-file">
          <Button variant="contained" color="primary" component="span">
            Upload
          </Button>
        </label>
        <Input className={classes.search_name_input} 
        placeholder="Search by name" 
        value={searchName} 
        onChange={e => setSearchName(e.target.value)}/>
      </div>
    </div>
  );
}

export default App;

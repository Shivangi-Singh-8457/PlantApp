import { Component, OnInit } from '@angular/core';
import { HttpClientService } from '../service/http-client.service';
import {Router} from '@angular/router';
import { User } from '../user';
import { FormGroup, NgForm } from '@angular/forms';
//import { Variable } from '@angular/compiler/src/render3/r3_ast';

var baseData = "";

@Component({
  selector: 'app-addleaf',
  templateUrl: './addleaf.component.html',
  styleUrls: ['./addleaf.component.scss']
})
export class AddleafComponent implements OnInit {
  sendres:any
  srcData:any
  fileToUpload: any=[];
  plantName:any
  userModel=new User('','','');
  
  constructor(private httpClient:HttpClientService) { 
    
  }

  ngOnInit(): void {
  }

  onChange(event: any) {
    console.log(event);
    for(var i=0; i<event.target.files.length; i++){
      this.fileToUpload.push(event.target.files[i]);
    }
    console.log(this.fileToUpload);
  }
  /*onChangetext() {
      var x=<HTMLInputElement>document.getElementById('plant');
      this.plantName=x.value;
      console.log(this.plantName);
  }*/
  
  onsubmit()
  {
    this.httpClient.sendimgname(this.plantName).subscribe(
      res=>{
        
      })  
    this.httpClient.sendfiledata(this.userModel).subscribe(
      res=>{
      })
      for(var i=0;i<this.fileToUpload.length;i++){
      this.httpClient.sendimagedata(this.fileToUpload[i]).subscribe(
        res=>{
          this.sendres=res; 
        })
      }
      alert(this.sendres);
      window.location.reload();
  }
}



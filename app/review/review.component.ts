import { Component, OnInit, Output, Input} from '@angular/core';
import { NgForm } from '@angular/forms';
import { Router } from '@angular/router';
import { HttpClientService } from '../service/http-client.service';

@Component({
  selector: 'app-review',
  templateUrl: './review.component.html',
  styleUrls: ['./review.component.scss'],
  //changeDetection:ChangeDetectionStrategy.OnPush
})
export class ReviewComponent implements OnInit {

  folderlist:any=[];
  imagelist:any={};
  comments:any={};
  arr: any=[];
  result:any;
  login_flag:any;
  msg:any;
  //isCollapsed = true; 
  
  
  constructor(private httpClient:HttpClientService, private router:Router){
    this.httpClient.checksignin().subscribe(
      res=>{
        this.login_flag=res
        console.log(this.login_flag);
    });
  }

  ngOnInit(): void {
    this.httpClient.getfolders().subscribe(
      res=>{
        this.folderlist=res[0];
        this.imagelist=res[1];
        //this.folderlist=this.folderlist.map((folder: { isCollapsed: boolean; })=>folder.isCollapsed=false)
        console.log(this.folderlist,this.imagelist)
      }
     )
    //this.folderlist=this.folderlist.map((folder: { isCollapsed: boolean; })=>folder.isCollapsed=true)
  }
  folderVote(id:any, ch:any)
  {
    if(this.login_flag)
    this.httpClient.folder_vote([id,ch]).subscribe(res=>{});
    else
    this.router.navigate(['login']);
  }
 imgVote(id:any, ind:any, ch:any){
  if(this.login_flag)
    this.httpClient.image_vote([id,ind,ch]).subscribe(res=>{});
  else
    this.router.navigate(['login']);
 }
 fetchComments(id:any)
 {
    this.httpClient.get_comments(id).subscribe(res=>{this.comments[id]=res});
 }
 saveComment(commentform:NgForm, id:any)
 {
  if(this.login_flag)
  {
    //console.log(this.msg);
    this.httpClient.save_comment([id,this.msg]).subscribe(res=>{});
    commentform.reset();
  }
  else
    this.router.navigate(['login']);
 }
  // async wait()
  // {
  //   await new Promise(resolve=>setTimeout(resolve,250));
  // }
  // createArray(id:any){
  //   console.log("create Array");
  //   this.arr=[];
  //   var i=1;
  //   while(i<=4)
  //   {
  //     this.arr.push(i);
  //     i++;
  //   }    
  //   //this.wait();  
  //   return this.arr;
  // }

  // createArray(id:any){
  //   console.log("create Array");
  //   this.httpClient.getArray(id).subscribe(
  //     res=>{
  //       this.arr=res
  //       console.log(this.arr)
  //     }
  //   )
  //   this.wait();  
  //   return this.arr;
  // }
  
  
}

import { Component, OnInit, Input, ViewChild} from '@angular/core';
import { RecipeEditorService } from '../../recipe-editor/recipe-editor.service';
import { RouterModule, Routes } from '@angular/router';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.css']
})
export class ResultComponent implements OnInit {
  @Input('searchResult') searchResult;
  @ViewChild('imgSrc') imgSrc;

  tiny_image = "https://bulma.io/images/placeholders/128x128.png"

  constructor(private recipeEditorService: RecipeEditorService) { }

  ngOnInit(): void {
    /*
    var promise = this.recipeEditorService.getRecipeImagesFromID(this.searchResult["dc_id"])
    
    promise.then(
      (val) => this.recivedImage(val),
      (err) => console.error(err)
    )*/

  }
  
  recivedImage(images) {
    console.log(this.imgSrc)
    if(Object.keys(images).length >= 1) {
      this.imgSrc.nativeElement.src = images[0]
    }
    
  }

}

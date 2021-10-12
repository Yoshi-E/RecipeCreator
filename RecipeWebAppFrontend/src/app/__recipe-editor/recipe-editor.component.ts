import { NgModule, Component, OnInit } from '@angular/core';
import {IngredientEditorComponent } from './ingredient-editor/ingredient-editor.component';


@NgModule({  
  declarations: [RecipeEditorComponent, IngredientEditorComponent],  
  imports: [    
  ],  
  exports: [RecipeEditorComponent]  
})  


@Component({
  selector: 'app-recipe-editor',
  templateUrl: './recipe-editor.component.html',
  styleUrls: ['./recipe-editor.component.css']
})
export class RecipeEditorComponent implements OnInit {

  public IngredientEditor: IngredientEditorComponent;
  constructor() { }

  ngOnInit(): void {
  }

}

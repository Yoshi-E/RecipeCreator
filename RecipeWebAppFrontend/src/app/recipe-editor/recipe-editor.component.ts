import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { RecipeEditorService } from './recipe-editor.service';

@Component({
  selector: 'app-recipe-editor',
  templateUrl: './recipe-editor.component.html',
  providers: [RecipeEditorService],
  styleUrls: ['./recipe-editor.component.css']
})

export class RecipeEditorComponent implements OnInit {
  recipeLoad
  recipeId = ""

  constructor(private activatedRoute: ActivatedRoute,
    private recipeEditor: RecipeEditorService) {
    this.recipeLoad = recipeEditor.recipeLoad //Get values from service

    this.activatedRoute.queryParams.subscribe(params => {
      if ("id" in params) {
        let id = params["id"]
        this.recipeId = id
        //Load recipe
        var promise = this.recipeEditor.getRecipeFromID(id)

        promise.then(
          (val) => this.recipeEditor.loadRecipe(val),
          (err) => this.recipeEditor.alertService.error('Error: '+err.status+' '+err.statusText)
        )
      }
      // Print the parameter to the console. 
    });
  }

  ngOnInit(): void {
    
  }

}

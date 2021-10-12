import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
//import { RecipeEditorComponent} from './recipe-editor.component'
import { IngredientEditorComponent } from './ingredient-editor/ingredient-editor.component';
import { TopicComponent } from './topic/topic.component';


@NgModule({
  declarations: [
        IngredientEditorComponent,
        TopicComponent],
  imports: [
    CommonModule
  ],
  exports: [IngredientEditorComponent,
            TopicComponent]
})
export class RecipeEditorModule { }

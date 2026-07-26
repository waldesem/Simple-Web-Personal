<script setup lang="ts">
import { resolveComponent, ref, type PropType } from "vue";
import type {
  user as userForm,
  person as personForm,
  itemsForms,
  FormElemAttrs,
} from "@/schema/forms";
import { Items, Person, User } from "@/types";

const emit = defineEmits(["submit"]);

const { fields, item } = defineProps({
  fields: {
    type: Array as PropType<
      | typeof userForm
      | typeof personForm
      | (typeof itemsForms)[keyof typeof itemsForms]
    >,
    required: true,
  },
  item: {
    type: Object as PropType<User | Person | Items[keyof Items]>,
    default: () => ({}),
  },
});

const form = ref(item);

const matchComponent = (element: keyof FormElemAttrs = "input") => {
  const html = {
    input: resolveComponent("UInput"),
    select: resolveComponent("USelect"),
    textarea: resolveComponent("UTextarea"),
  };
  return html[element];
};
</script>

<template>
  <UForm :state="form" @submit.prevent="emit('submit', form)">
    <UFormField
      v-for="field in fields"
      :key="field.key"
      :label="field.label"
      :name="field.key"
      :required="field.props.required ?? false"
    >
      <component
        :is="matchComponent(field.element)"
        v-model.lazy.trim="form[field.key as keyof typeof form]"
        v-bind="field.props"
      />
    </UFormField>
    <UButton label="Принять" color="success" variant="outline" type="submit" />
  </UForm>
</template>

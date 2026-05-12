<script setup lang="ts">
import { PropType } from "vue";
import type { Contact, ItemField } from "@/types";

const props = defineProps({
  item: {
    type: Object as PropType<Contact>,
    required: true,
  },
});

const fields = [
  { key: "view", label: "Вид", value: props.item.view },
  { key: "contact", label: "Контакт", value: props.item.contact },
] as ItemField[];
</script>

<template>
  <ItemCard :fields="fields" />
</template>

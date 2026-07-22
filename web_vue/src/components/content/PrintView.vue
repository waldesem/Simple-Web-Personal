<script setup lang="ts">
import { type PropType } from "vue";
import { accordion, person as PersonField, itemsFields } from "@/schema/items";
import { ItemsArray, Person } from "@/types";
import ItemRow from "./ItemRow.vue";

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    default: () => ({}),
  },
  datas: {
    type: Object as PropType<ItemsArray>,
    default: () => ({}),
  },
});

const print = defineModel();
</script>

<template>
  <UButton
    class="absolute right-10 no-print"
    icon="i-lucide-x"
    variant="ghost"
    @click="print = false"
  />
  <div class="uppercase text-xl font-bold underline mb-6">
    {{
      `${props.person.surname} ${props.person.firstname} ${props.person.patronymic ?? ""}`
    }}
  </div>

  <template v-for="(field, index) in PersonField.slice(3)" :key="index">
    <ItemRow
      v-if="props.person[field.key] && !field.slot"
      :data="props.person"
      :field="field"
    />
  </template>

  <div class="mt-6 border-dashed border-b" />

  <template v-for="(accord, index) in accordion" :key="index">
    <div
      v-if="datas[accord.slot]"
      class="font-bold tracking-wider underline mt-6"
    >
      {{ accord.label }}
    </div>
    <template v-if="datas[accord.slot] && Array.isArray(datas[accord.slot])">
      <div
        class="my-3 border-dashed border-b"
        v-for="(data, idx) in datas[accord.slot]"
        :key="idx"
      >
        <template v-for="(field, ix) in itemsFields[accord.slot]" :key="ix">
          <ItemRow
            v-if="data[field.key as keyof typeof data]"
            :data="data"
            :field="field"
          />
        </template>
      </div>
    </template>
  </template>
</template>

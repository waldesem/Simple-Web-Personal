<script setup lang="ts">
import type { PropType } from "vue";
import { accordion, person as PersonField, itemsFields } from "@/schema/items";
import { ItemsArray, Person } from "@/types";
import ItemRow from "./ItemRow.vue";

const props = defineProps({
  person: {
    type: Object as PropType<Person>,
    required: true,
  },
  datas: {
    type: Object as PropType<ItemsArray>,
    required: true,
  },
});

const print = defineModel();
</script>

<template>
  <UButton
    class="absolute right-0 no-print"
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

  <USeparator class="mt-6 px-2" />

  <UCollapsible
    v-for="(accord, index) in accordion"
    :key="index"
    :unmount-on-hide="false"
    default-open
  >
    <UButton
      v-if="datas[accord.slot].length"
      variant="ghost"
      trailing-icon="i-lucide-chevron-down"
      color="neutral"
      size="xl"
      class="group font-bold tracking-wider underline my-2"
      :ui="{
        base: 'px-1',
        trailingIcon:
          'group-data-[state=closed]:rotate-180 transition-transform duration-200',
      }"
    >
      {{ accord.label }}
    </UButton>
    <template
      #content
      v-if="datas[accord.slot] && Array.isArray(datas[accord.slot])"
    >
      <UCollapsible
        v-for="(data, idx) in datas[accord.slot]"
        :key="idx"
        :unmount-on-hide="false"
        default-open
        class="collapsible-root-wrapper"
      >
        <template #content>
          <template v-for="(field, ix) in itemsFields[accord.slot]" :key="ix">
            <ItemRow
              v-if="data[field.key as keyof typeof data]"
              :data="data"
              :field="field"
            />
          </template>
        </template>
        <template #default>
          <UButton class="group" variant="ghost" color="neutral" block>
            <USeparator
              icon="i-lucide-chevron-down"
              :ui="{
                icon: 'group-data-[state=closed]:rotate-180 transition-transform duration-200',
              }"
            />
          </UButton>
        </template>
      </UCollapsible>
    </template>
  </UCollapsible>
</template>

<style scoped>
@media print {
  div[data-state="closed"],
  .iconify {
    display: none !important;
    visibility: hidden;
  }
}

.collapsible-root-wrapper {
  display: flex;
  flex-direction: column;
}

[data-slot="content"] {
  order: 1;
}
[data-slot="base"] {
  order: 2;
}
</style>

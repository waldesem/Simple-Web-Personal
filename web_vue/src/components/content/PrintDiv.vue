<script setup lang="ts">
import { type PropType } from "vue";
import { accordion, person as PersonField, itemsFields } from "@/schema/items";
import { ItemsArray, Person } from "@/types";

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

const emit = defineEmits(["print"]);
</script>

<template>
  <UButton
    class="absolute right-10 no-print"
    icon="i-lucide-x"
    variant="ghost"
    @click="emit('print')"
  />
  <div class="uppercase text-xl font-bold underline mb-6">
    {{
      `${props.person.surname} ${props.person.firstname} ${props.person.patronymic ?? ""}`
    }}
  </div>

  <div v-for="(field, index) in PersonField" :key="index">
    <div
      v-if="
        props.person[field.key] &&
        !field.slot &&
        !field.component &&
        !['surname', 'firstname', 'patronymic'].includes(field.key)
      "
      class="grid grid-cols-12 gap-4 mb-4"
    >
      <div class="col-span-3">{{ field.label }}</div>
      <div class="col-span-9 wrap-break-word">
        <span>
          {{ field.foo ? field.foo(props.person) : props.person[field.key] }}
        </span>
      </div>
    </div>
  </div>

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
          <div
            v-if="
              data[field.key as keyof typeof data] &&
              !field.slot &&
              !field.component
            "
            class="grid grid-cols-12 gap-4 mb-4"
          >
            <div class="col-span-3">{{ field.label }}</div>
            <div class="col-span-9 wrap-break-word">
              <span>
                {{
                  field.foo
                    ? field.foo(data as any)
                    : data[field.key as keyof typeof data]
                }}
              </span>
            </div>
          </div>
        </template>
      </div>
    </template>
  </template>
</template>

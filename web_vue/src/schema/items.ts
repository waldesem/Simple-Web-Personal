import { h } from "vue";
import { conclusions, decisions, localStr } from "@/utils";
import type { ItemField, Items } from "@/types";

const addresses = [
  { key: "view", label: "Вид адреса" },
  { key: "address", label: "Адрес" },
] as ItemField[];

const affilations = [
  { key: "view", label: "Вид участия" },
  { key: "organization", label: "Организация" },
  { key: "inn", label: "ИНН" },
  { key: "activity", label: "Деятельность" },
] as ItemField[];

const checks = [
  { key: "workplace", label: "Проверка по местам работы" },
  { key: "document", label: "Проверка документов" },
  { key: "debt", label: "Проверка задолженностей" },
  { key: "bankruptcy", label: "Проверка банкротства" },
  { key: "bki", label: "Проверка Кредитной истории" },
  { key: "courts", label: "Проверка судебных дел" },
  { key: "affilation", label: "Проверка аффилированности" },
  { key: "terrorist", label: "Проверка в списке террористов" },
  { key: "internet", label: "Проверка в открытых источниках" },
  { key: "cronos", label: "Проверка в Кронос" },
  { key: "addition", label: "Дополнительная информация" },
  { key: "comment", label: "Комментарий" },
  {
    key: "conclusion",
    label: "Результат",
    component: (val: string) => {
      const color =
        val === conclusions.agreed
          ? "bg-green-500"
          : val === conclusions.cancel
            ? "bg-gray-500"
            : val === conclusions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return () =>
        h(
          "div",
          {
            class: [
              "flex",
              "items-center",
              "inline-flex",
              "py-1 px-2",
              "rounded-md",
              "text-sm",
              "text-white",
              color,
            ],
          },
          val,
        );
    },
  },
  { key: "created", label: "Дата записи", div: (div) => localStr(div) },
] as ItemField[];

const contacts = [
  { key: "view", label: "Вид контакта" },
  { key: "contact", label: "Контакт" },
] as ItemField[];

const documents = [
  { key: "view", label: "Вид документа" },
  { key: "series", label: "Серия документа" },
  { key: "digits", label: "Номер документа" },
  { key: "agency", label: "Кем выдан" },
  { key: "issue", label: "Дата выдачи", div: (div) => localStr(div) },
] as ItemField[];

const educations = [
  { key: "view", label: "Вид образования" },
  { key: "institution", label: "Учебное заведение" },
  { key: "finished", label: "Год окончания" },
  { key: "specialty", label: "Специальность" },
] as ItemField[];

const inquiries = [
  { key: "info", label: "Информация" },
  { key: "initiator", label: "Инициатор" },
  { key: "created", label: "Дата записи", div: (div) => localStr(div) },
] as ItemField[];

const investigations = [
  { key: "theme", label: "Тема проверки" },
  { key: "info", label: "Информация" },
  { key: "created", label: "Дата записи", div: (div) => localStr(div) },
] as ItemField[];

const poligrafs = [
  { key: "theme", label: "Тема проверки" },
  { key: "results", label: "Результат" },
  {
    key: "conclusion",
    label: "Результат",
    component: (val: string) => {
      const color =
        val === decisions.agreed
          ? "bg-green-500"
          : val === decisions.cancel
            ? "bg-gray-500"
            : val === decisions.comments
              ? "bg-blue-500"
              : "bg-red-500";
      return () =>
        h(
          "div",
          {
            class: [
              "flex",
              "items-center",
              "inline-flex",
              "py-1 px-2",
              "rounded-md",
              "text-sm",
              "text-white",
              color,
            ],
          },
          val,
        );
    },
  },
  { key: "created", label: "Дата записи", div: (div) => localStr(div) },
] as ItemField[];

const previous = [
  { key: "surname", label: "Фамилия" },
  { key: "firstname", label: "Имя" },
  { key: "patronymic", label: "Отчество" },
  { key: "changed", label: "Год изменения" },
  { key: "reason", label: "Причина" },
] as ItemField[];

const staffs = [
  { key: "position", label: "Должность" },
  { key: "department", label: "Подразделение" },
] as ItemField[];

const workplaces = [
  { key: "nowWork", label: "Текущая работа" },
  { key: "starts", label: "Начало работы", div: (div) => localStr(div) },
  { key: "finished", label: "Окончание работы", div: (div) => localStr(div) },
  { key: "workplace", label: "Место работы" },
  { key: "position", label: "Должность" },
  { key: "address", label: "Адрес организации" },
  { key: "reason", label: "Причина увольнения" },
] as ItemField[];

export const itemFields = {
  addresses,
  affilations,
  checks,
  contacts,
  documents,
  educations,
  inquiries,
  investigations,
  poligrafs,
  previous,
  staffs,
  workplaces,
} as { [key in keyof Items]: ItemField[] };

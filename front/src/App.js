import React, { useState, useEffect } from "react";
import ResultTable from "./components/Table";
import { Form, Input, Button, Select, InputNumber } from "antd";
import "./App.css";

const config = (initialValue, required) => ({
  initialValue,
  validate: [
    {
      trigger: "onChange",
      rules: [
        {
          required: required,
          message: "Поле, обязательное для заполнения"
        }
      ]
    }
  ]
});

function App({ form }) {
  useEffect(() => {
    console.log(result);
    console.log(loading);
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState([]);

  const getData = async () => {
    setLoading(true);
    const dataJson = await fetch("/api/news").then(response => response.json());
    setLoading(false);
    setResult(dataJson);
  };

  const onSubmit = e => {
    e.preventDefault();
    form.validateFields((err, values) => {
      if (!err) {
        getData();
        console.log(values);
      }
    });
  };

  return (
    <div className="App">
      <header className="App-header">
        <Form className="Main-form">
          <div>
            <span className="label">
              Сайт/Блог для парсинга
              <br />
              вконце без слеша
            </span>
            <Form.Item onSubmit={onSubmit}>
              {form.getFieldDecorator(
                "site",
                config("https://pasmi.ru/cat/news", true)
              )(<Input placeholder="Укажите сайт" className="md" />)}
            </Form.Item>
          </div>
          <div>
            <span className="label">Тэг главного контейнера</span>
            <Form.Item>
              {form.getFieldDecorator("containerTag", config("article", true))(
                <Input
                  className="sm"
                  placeholder="Укажите тэг контейнера новости"
                />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">Класс главного контейнера</span>
            <Form.Item>
              {form.getFieldDecorator(
                "containerClass",
                config("preview", false)
              )(
                <Input
                  className="sm"
                  placeholder="Укажите класс контейнера новости"
                />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">Заголовка(по умолчанию h1)</span>
            <Form.Item>
              {form.getFieldDecorator("titleTag", config("h1", true))(
                <Input className="sm" placeholder="Укажите тэг заголовка" />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">
              Класс Заголовка
              <br />
              (необязательно)
            </span>
            <Form.Item>
              {form.getFieldDecorator("titleClass", config("", false))(
                <Input className="sm" placeholder="Укажите тэг заголовка" />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">
              Укажите в котором тэги
              <br /> ссылки на страницы
            </span>
            <Form.Item>
              {form.getFieldDecorator("pageContainer", config("div", false))(
                <Input className="sm" placeholder="Укажите <тэг>" />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">
              Укажите класс контайнера для страниц
              <br /> (необязательно)
            </span>
            <Form.Item>
              {form.getFieldDecorator(
                "pageContainerСlass",
                config("nav-links", false)
              )(<Input className="sm" placeholder="Укажите <тэг>" />)}
            </Form.Item>
          </div>
          <div>
            <span className="label">Формат страниц</span>
            <Form.Item>
              {form.getFieldDecorator("pageFormat", config("/page/", false))(
                <Select placeholder="Укажите формат страниц" className="sm">
                  <Select.Option value="/page/" key="/page/">
                    /page/
                  </Select.Option>
                  <Select.Option value="?page=" key="?page=">
                    ?page=
                  </Select.Option>
                </Select>
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">Сколько стр. парсить?</span>
            <Form.Item>
              {form.getFieldDecorator("pageCount", {})(
                <InputNumber
                  className="sm"
                  placeholder="Укажите число (необязательно)"
                />
              )}
            </Form.Item>
          </div>
          <div>
            <span className="label">
              Класс времени новости
              <br />
              (необязательно)
            </span>
            <Form.Item>
              {form.getFieldDecorator("timeClass", config("time", false))(
                <Input
                  className="sm"
                  placeholder="Укажите класс времени новости"
                />
              )}
            </Form.Item>
          </div>
          <div>
            <Button onClick={onSubmit} type="primary">
              Попробывать (парсинг)
            </Button>
          </div>
        </Form>
      </header>
      <ResultTable result={result} loading={loading} />
      <Button type="danger" id="clear" onClick={() => setResult([])}>
        Очисть результаты
      </Button>
    </div>
  );
}

export default Form.create()(App);

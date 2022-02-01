import React from "react";
import { Card, CardBody, CardTitle } from "reactstrap";
import Drink from "./menuItemCounter";

function Home() {
  return (
    <section className="col-md-8">
      <Card>
        <CardBody className="text-center">
          <Drink />
          <CardTitle>
            <h3 className="font-weight-bold">
              Welcome to Silicon Valley's premier dive cafe!
            </h3>
          </CardTitle>
        </CardBody>
      </Card>
    </section>
  );
}

export default Home;
